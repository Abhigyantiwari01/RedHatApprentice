from pymongo import MongoClient
import os

CONNECTION_STRING = os.environ["MONGO_URL"]

"""
Creates and returns a new database object
"""
def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client['pizza_house']

