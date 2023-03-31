from fastapi import FastAPI, HTTPException
import uuid
from datetime import datetime
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser(description='Start the service on two servers.')
parser.add_argument('primary', help='IP address of the primary DB')
parser.add_argument('secondary', help='IP address of the secondary DB')
args = parser.parse_args()
primary = args.primary
secondary = args.secondary
app = FastAPI()


class Task():
    def __init__(self, description: str, headline: str):
        self.headline = headline
        self.description = description
        self.creation_time = datetime.now()
        self.task_id = str(uuid.uuid4())

    def create_dict(self):
        data = {
            "headline": self.headline,
            "description": self.description,
            "creation_time": self.creation_time.isoformat(),
            "task_id": self.task_id
        }
        return data


class DBConnection():
    def __init__(self, client: str):
        self.client = MongoClient(f'mongodb://{client}:27017/')
        self.db = self.client['database']
        self.tasks = self.db['tasks']


primary_db = DBConnection(primary)
secondary_db = DBConnection(secondary)


# need to change to post at the end
@app.post("/tasks/create_task")
async def create_task(headline: str, description: str):
    new_task = Task(headline, description)

    # Insert the new task into the primary database
    result_primary = primary_db.tasks.insert_one(new_task.create_dict())

    # Insert the new task into the secondary database
    result_secondary = secondary_db.tasks.insert_one(new_task.create_dict())

    # Check that the task was successfully added to both databases
    if result_primary.inserted_id and result_secondary.inserted_id:
        return {"message": "Task added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add task")


@app.get("/tasks/get_tasks")
async def get_tasks():
    tasks = []
    all_tasks = primary_db.tasks.find()
    for task in all_tasks:
        tasks.append(task)
    return {"tasks": tasks}


@app.delete("/tasks/remove_task")
async def remove_task(task_id: str):
    result_primary = primary_db.tasks.delete_one({"task_id": task_id})

    # Delete the task from the secondary database
    result_secondary = secondary_db.tasks.delete_one({"task_id": task_id})

    # Check that the task was successfully deleted from both databases
    if result_primary.deleted_count and result_secondary.deleted_count:
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")


def main():
    pass


if __name__ == '__main__':
    main()
