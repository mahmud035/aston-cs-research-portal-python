from fastapi import APIRouter, Query, Depends
from typing import Dict, Any, Optional
from pymongo.database import Database
from app.core.utils import send_response
from app.modules.search import service
from app.core.db import get_db


router = APIRouter()


@router.get("/", response_model=dict)
def search(
    q: str = Query(..., min_length=1),
    limit: Optional[int] = Query(20),
    offset: Optional[int] = Query(0),
    db: Database = Depends(get_db),
) -> Dict[str, Any]:
    pubs = service.search_publications(db, q, limit=limit, offset=offset)
    facs = service.search_faculties(db, q, limit=limit, offset=offset)

    return send_response(
        {"publications": pubs, "faculties": facs},
        status_code=200,
        message="Search results retrieved successfully",
        meta={"total": len(pubs) + len(facs)},
    )
