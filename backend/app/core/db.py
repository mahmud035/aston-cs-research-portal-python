from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "aston_cs_research_portal")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def get_db() -> Database:
    """
    Dependency for route handlers to get MongoDB database handle.
    """
    return db
