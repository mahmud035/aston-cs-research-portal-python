from functools import lru_cache
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "aston_cs_research_portal")


@lru_cache(maxsize=1)
def get_client():
    return MongoClient(MONGO_URI)


def get_db():
    return get_client()[DB_NAME]
