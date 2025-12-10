from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pymongo.database import Database
from app.core.utils import send_response
from app.modules.faculty import service, schemas
from app.main import get_db

router = APIRouter()

@router.get("/{faculty_id}", response_model=dict)
def get_faculty(faculty_id: str, db: Database = Depends(get_db)):
    """
    GET /api/v1/faculties/{faculty_id}
    Returns full faculty profile: departments, publications (articles & conference)
    """
    faculty = service.get_faculty_by_id(db, faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    departments = []
    if faculty.get("departmentIds"):
        departments = service.get_departments_by_ids(db, faculty["departmentIds"])

    publications = []
    if faculty.get("articleIds") or faculty.get("conferencePaperIds"):
        ids = []
        if faculty.get("articleIds"):
            ids.extend(faculty["articleIds"])
        if faculty.get("conferencePaperIds"):
            ids.extend(faculty["conferencePaperIds"])
        publications = service.get_publications_by_ids(db, ids)

    # split into articles and conferences
    articles = [p for p in publications if p.get("kind") == "article"]
    conferences = [p for p in publications if p.get("kind") == "conference"]

    result = {
        "_id": faculty["_id"],
        "name": faculty.get("name"),
        "position": faculty.get("position"),
        "researchInterest": faculty.get("researchInterest"),
        "departments": departments,
        "articles": articles,
        "conferencePapers": conferences,
    }

    return send_response(result, status_code=200, message="Faculty retrieved successfully")
