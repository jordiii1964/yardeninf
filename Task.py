import uuid
from datetime import datetime


class Task():
    def __init__(self, headline: str, description: str):
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
