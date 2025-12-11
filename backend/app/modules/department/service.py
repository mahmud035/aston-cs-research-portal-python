from typing import List, Optional
from pymongo.database import Database
from bson import ObjectId

DEPARTMENT_COLLECTION = "departments"
FACULTY_COLLECTION = "faculties"


def get_all_departments(db: Database) -> List[dict]:
    cursor = db[DEPARTMENT_COLLECTION].find(
        {"isComputerScienceRelated": True},
        {"name": 1, "slug": 1},
    )
    return [
        {"_id": str(d["_id"]), "name": d["name"], "slug": d["slug"]} for d in cursor
    ]


def get_department_by_slug(db: Database, slug: str) -> Optional[dict]:
    doc = db[DEPARTMENT_COLLECTION].find_one(
        {
            "slug": slug,
            "isComputerScienceRelated": True,
        }
    )
    if not doc:
        return None

    return {
        "_id": str(doc["_id"]),
        "name": doc.get("name"),
        "slug": doc.get("slug"),
        "type": doc.get("type"),
        "description": doc.get("description"),
        "isComputerScienceRelated": doc.get("isComputerScienceRelated"),
    }


def get_faculties_for_department(db: Database, dept_id: str) -> List[dict]:
    """
    Fetch all faculties whose departmentIds contain the given department ObjectId
    """
    try:
        oid = ObjectId(dept_id)
    except Exception:
        return []

    cursor = db[FACULTY_COLLECTION].find(
        {"departmentIds": {"$in": [oid]}}, {"name": 1, "position": 1}
    )

    faculties = []
    for f in cursor:
        faculties.append(
            {"_id": str(f["_id"]), "name": f.get("name"), "position": f.get("position")}
        )
    return faculties
