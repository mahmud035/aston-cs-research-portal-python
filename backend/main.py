import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from pymongo import MongoClient
from pymongo.database import Database

from app.core.error_handlers import http_error_handler, mongo_error_handler
from app.modules.department.controller import router as department_router
from app.modules.faculty.controller import router as faculty_router

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

app = FastAPI(title="Aston CS Research Portal API")

# Register routers
app.include_router(department_router, prefix="/api/v1/departments", tags=["departments"])
app.include_router(faculty_router, prefix="/api/v1/faculties", tags=["faculties"])

# Register exception handlers
app.add_exception_handler(Exception, mongo_error_handler)
app.add_exception_handler(HTTPException, http_error_handler)
