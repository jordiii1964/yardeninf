import uuid
from datetime import datetime


class Task():
    """
          Creates a Task object with the given headline and description.

          Args:
              headline (str): The headline of the task.
              description (str): The description of the task.
          """

    def __init__(self, headline: str, description: str):
        self.headline = headline
        self.description = description
        self.creation_time = datetime.now()
        self.task_id = str(uuid.uuid4())

    def create_dict(self):
        """
               Returns a dictionary of the Task object. The dict is made due to the fact MongoDB needs to get values in a dict format.

        """
        data = {
            "headline": self.headline,
            "description": self.description,
            "creation_time": self.creation_time.isoformat(),
            "task_id": self.task_id
        }
        return data
