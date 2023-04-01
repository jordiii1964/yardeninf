from pymongo import MongoClient


class DB_Connection():
    def __init__(self, client: str):
        self.client = MongoClient(f'mongodb://{client}:27017/')
        self.db = self.client['database']
        self.tasks = self.db['tasks']

    def close_session(self):
        self.client.close()
