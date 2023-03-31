from fastapi import FastAPI, HTTPException
import uuid
from datetime import datetime
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser(description='Start the service on two servers.')
parser.add_argument('primary', help='IP address of the primary server')
parser.add_argument('secondary', help='IP address of the secondary server')
args = parser.parse_args()
primary = args.primary
secondary = args.secoundery
app = FastAPI()


class Task():
    def __init__(self, description: str, headline: str):
        self.headline = headline
        self.description = description
        self.creation_time = datetime.now()
        self.task_id = str(uuid.uuid4())


# connect to primary database
primary_client = MongoClient(f'mongodb://{primary}:27017/')
primary_db = primary_client['myproject']
primary_tasks = primary_db['tasks']

# connect to second database
secondary_client = MongoClient(f'mongodb://{secondary}:27017/')
secondary_db = secondary_client['myproject']
secondary_tasks = secondary_db['tasks']


# need to change to post at the end
@app.post("/tasks/create_task")
async def create_task(headline: str, description: str):
    new_task = Task(headline, description)

    # Insert the new task into the primary database
    result_primary = primary_tasks.insert_one(new_task.dict())

    # Insert the new task into the secondary database
    result_secondary = secondary_tasks.insert_one(new_task.dict())

    # Check that the task was successfully added to both databases
    if result_primary.inserted_id and result_secondary.inserted_id:
        return {"message": "Task added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add task")


@app.get("/tasks/get_tasks")
async def get_tasks():


# @app.delete("tasks/remove_task")
# async def remove_task(headline: str, assigned_to: str):
def main():
    pass

if __name__ == '__main__':
    main()
