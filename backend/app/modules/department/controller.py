from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from typing import Dict, Any

from app.core.utils import send_response
from . import service
from app.core.db import get_db

router = APIRouter()


@router.get("/", response_model=dict)
def list_departments(db: Database = Depends(get_db)):
    depts = service.get_all_departments(db)
    return send_response(
        depts, status_code=200, message="Departments retrieved successfully"
    )


@router.get("/{slug}", response_model=dict)
def get_department(slug: str, db: Database = Depends(get_db)) -> Dict[str, Any]:
    """
    GET /api/v1/departments/{slug}
    Returns a department with all its faculties
    """
    dept = service.get_department_by_slug(db, slug)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    # fetch faculties in this department
    faculties = service.get_faculties_for_department(db, dept["_id"])

    return send_response(
        {
            "_id": dept["_id"],
            "name": dept["name"],
            "slug": dept["slug"],
            "type": dept.get("type"),
            "description": dept.get("description"),
            "isComputerScienceRelated": dept.get("isComputerScienceRelated", True),
            "faculties": faculties,
        },
        status_code=200,
        message=f"Faculties for department '{dept['name']}' retrieved successfully",
        meta={"total": len(faculties)},
    )
