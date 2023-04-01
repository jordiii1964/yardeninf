from fastapi import FastAPI, HTTPException, Form, Query
import argparse
import uvicorn
from db_connection import DB_Connection
from task import Task

app = FastAPI()


@app.post("/tasks/create_task")
async def create_task(headline: str = Form(...), description: str = Form(...)):
    """
    This function creates a new task and inserts it into both databases.
    :param headline: str
        The headline of the new task.
    :param description: str
        The description of the new task.
    :return: dict
        A message indicating whether the task was added successfully or not to both of the databases.
    """
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
    """
    This function gets all the tasks from the primary database.
    :return: dict
        A dictionary with all of the tasks.
    """
    tasks = []
    all_tasks = primary_db.tasks.find()
    for task in all_tasks:
        task_dict = dict(task)
        task_dict['_id'] = str(task_dict['_id'])  # convert ObjectId to string
        tasks.append(task_dict)
    return {"tasks": tasks}


@app.get("/tasks/search_task")
async def search_task(task_headline: str = Query(...)):
    """
       This function searches for tasks with the given headline in the primary database.
       :param task_headline: str
           The headline to search for.
       :return: dict
           A dictionary of the tasks with the given headline.
       """
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
    """
      This function removes a task with the given ID from both databases.
      :param task_id: str
          The ID of the task to remove (it's the uuid)
      :return: dict
          A message indicating whether the task was deleted successfully or not from both of the databases.
      """

    result_primary = primary_db.tasks.delete_one({"task_id": task_id})

    # Delete the task from the secondary database
    result_secondary = secondary_db.tasks.delete_one({"task_id": task_id})

    # Check that the task was successfully deleted from both databases
    if result_primary.deleted_count and result_secondary.deleted_count:
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")


if __name__ == '__main__':
    # Define parser arguments to set the IP addresses of the primary and secondary databases
    parser = argparse.ArgumentParser(description='Start the service on two servers.')
    parser.add_argument('--primary', required=True, help='IP address of the primary DB')
    parser.add_argument('--secondary', required=True, help='IP address of the secondary DB')
    args = parser.parse_args()
    # Connect to the primary and secondary databases
    primary = args.primary
    secondary = args.secondary
    primary_db = DB_Connection(primary)
    secondary_db = DB_Connection(secondary)
    # Run the service using Uvicorn (due to using Fastapi)
    uvicorn.run(app, host='0.0.0.0', port=8000)
