from pymongo import MongoClient


class DB_Connection():
    """
    Connects to a MongoDB database using the specified client address, and creates a tasks collection.

    Args:
        client_address (str): The address of the MongoDB client to connect to.
    """
    def __init__(self, client: str):
        self.client = MongoClient(f'mongodb://{client}:27017/')
        self.db = self.client['database']
        self.tasks = self.db['tasks']


