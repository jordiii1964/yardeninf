from fastapi import FastAPI, HTTPException
import uuid
from datetime import datetime

app = FastAPI()


class Task():
    def __init__(self, description: str, username: str):
        #self.headline = headline
        self.description = description
        self.creation_time = datetime.now()
        self.task_id = str(uuid.uuid4())


headlines_to_tasks = {}
user_to_tasks = {}


@app.get("/tasks/create_task")
async def create_task(headline: str, description: str):
    try:
        task = Task(headline, description)

        if headline in tasks:
            # if it does, append the new task to the existing list
            tasks[headline].append(task)
        else:
            # if it doesn't, create a new array with the new task
            tasks[headline] = [task]
        return {"status_code": 201}
    except Exception:
        raise HTTPException(status_code=400, detail="try again!")


@app.get("/tasks/tasks_list")
async def tasks_list():
    return tasks


#@app.delete("tasks/remove_task")
#async def remove_task(headline: str, assigned_to: str):
