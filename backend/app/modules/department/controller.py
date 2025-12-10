from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pymongo.database import Database
from app.core.utils import send_response
from app.modules.department import service, schemas
from app.main import get_db  # function we’ll define in main to get DB handle

router = APIRouter()

@router.get("/", response_model=dict)
def list_departments(db: Database = Depends(get_db)):
    """
    Endpoint: GET /api/v1/departments/
    Returns list of all CS-related departments.
    """
    depts = service.get_all_departments(db)
    return send_response(depts, status_code=200, message="Departments retrieved successfully")

@router.get("/{slug}", response_model=dict)
def get_department(slug: str, db: Database = Depends(get_db)):
    """
    Endpoint: GET /api/v1/departments/{slug}
    Returns a department by slug + minimal info. Further faculty listing via frontend / other endpoints.
    """
    dept = service.get_department_by_slug(db, slug)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return send_response(dept, status_code=200, message="Department retrieved successfully")
