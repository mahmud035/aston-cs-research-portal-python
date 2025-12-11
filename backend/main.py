import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from app.core.error_handlers import http_error_handler, mongo_error_handler

from app.modules.department.controller import router as department_router
from app.modules.faculty.controller import router as faculty_router
from app.modules.publication.controller import router as publication_router
from app.modules.search.controller import router as search_router

from app.core.db import get_db  # <-- new import

load_dotenv()

app = FastAPI(title="Aston CS Research Portal API")

# Register routers
app.include_router(
    department_router, prefix="/api/v1/departments", tags=["departments"]
)
app.include_router(faculty_router, prefix="/api/v1/faculties", tags=["faculties"])
app.include_router(
    publication_router, prefix="/api/v1/publications", tags=["publications"]
)
app.include_router(search_router, prefix="/api/v1/search", tags=["search"])

# Register exception handlers
app.add_exception_handler(Exception, mongo_error_handler)
app.add_exception_handler(HTTPException, http_error_handler)
