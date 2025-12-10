from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pymongo.database import Database

from app.core.utils import send_response
from app.modules.publication import service, schemas
from app.main import get_db

router = APIRouter()

@router.get("/", response_model=dict)
def list_publications(db: Database = Depends(get_db)):
    """
    GET /api/v1/publications
    Return list of all publications (articles + conference papers), with minimal author info.
    """
    pubs = service.get_all_publications(db)
    return send_response(pubs, status_code=200, message="Publications retrieved successfully")

@router.get("/{pub_id}", response_model=dict)
def get_publication(pub_id: str, db: Database = Depends(get_db)):
    """
    GET /api/v1/publications/{pub_id}
    Return a single publication with details and authors.
    """
    pub = service.get_publication_by_id(db, pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")
    return send_response(pub, status_code=200, message="Publication retrieved successfully")
