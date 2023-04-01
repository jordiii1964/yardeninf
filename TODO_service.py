from fastapi import FastAPI, HTTPException, Form, Query
import argparse
import uvicorn
import DB_Connection
import Task

app = FastAPI()

parser = argparse.ArgumentParser(description='Start the service on two servers.')
parser.add_argument('--primary', required=True, help='IP address of the primary DB')
parser.add_argument('--secondary', required=True, help='IP address of the secondary DB')
args = parser.parse_args()
primary = args.primary
secondary = args.secondary
primary_db = DB_Connection(primary)
secondary_db = DB_Connection(secondary)


@app.post("/tasks/create_task")
async def create_task(headline: str = Form(...), description: str = Form(...)):
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


@app.get("/tasks/get_all_tasks")
async def get_all_tasks():
    tasks = []
    all_tasks = primary_db.tasks.find()
    for task in all_tasks:
        task_dict = dict(task)
        task_dict['_id'] = str(task_dict['_id'])  # convert ObjectId to string
        tasks.append(task_dict)
    return {"tasks": tasks}


@app.get("/tasks/search_task")
async def search_task(task_headline: str = Query(...)):
    # Search for tasks with the given name in both databases
    tasks = primary_db.tasks.find({"headline": task_headline})
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found with that headline")
    tasks = list(tasks)
    if len(tasks) > 0:
        tasks_list = []
        for task in tasks:
            task_id = task["task_id"]
            description = task["description"]
            creation_time = task["creation_time"]
            task_info = {"task_id": task_id, "description": description,
                         "creation_time": creation_time}
            tasks_list.append(task_info)
        return {"message": f"Here are the tasks with the headline '{task_headline}'", "tasks": tasks_list}

    else:
        return {"message": "No tasks found with the headline :("}


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


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
