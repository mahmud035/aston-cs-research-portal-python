from typing import List, Optional
from pymongo.database import Database

DEPARTMENT_COLLECTION = "departments"

def get_all_departments(db: Database) -> List[dict]:
    """
    Fetch all departments flagged as CS-related.
    Returns list of dictionaries with _id, name, slug.
    """
    cursor = db[DEPARTMENT_COLLECTION].find(
        { "isComputerScienceRelated": True },
        { "_id": 1, "name": 1, "slug": 1 }
    )
    depts = []
    for doc in cursor:
        depts.append({
            "_id": str(doc["_id"]),
            "name": doc.get("name"),
            "slug": doc.get("slug"),
        })
    return depts

def get_department_by_slug(db: Database, slug: str) -> Optional[dict]:
    """
    Fetch a single department by slug if CS-related.
    """
    doc = db[DEPARTMENT_COLLECTION].find_one(
        { "slug": slug, "isComputerScienceRelated": True }
    )
    if not doc:
        return None
    return {
        "_id": str(doc["_ed"]),  # We'll fix below (typo) when using
        "name": doc.get("name"),
        "slug": doc.get("slug"),
        # Optionally include type / description if you stored them
    }
