from typing import Optional, List
from pymongo.database import Database
from bson import ObjectId

FACULTY_COLLECTION = "faculties"
DEPARTMENT_COLLECTION = "departments"
PUBLICATION_COLLECTION = "publications"


def get_faculty_by_id(db: Database, faculty_id: str) -> Optional[dict]:
    try:
        oid = ObjectId(faculty_id)
    except Exception:
        return None

    doc = db[FACULTY_COLLECTION].find_one({"_id": oid})
    if not doc:
        return None

    doc["_id"] = str(doc["_id"])
    for key in ("departmentIds", "articleIds", "conferencePaperIds"):
        if key in doc and isinstance(doc[key], list):
            doc[key] = [str(x) for x in doc[key]]

    return doc


def get_departments_by_ids(db: Database, ids: List[str]) -> List[dict]:
    object_ids = []
    for s in ids:
        try:
            object_ids.append(ObjectId(s))
        except:
            continue

    cursor = db[DEPARTMENT_COLLECTION].find(
        {"_id": {"$in": object_ids}},
        {"name": 1, "slug": 1},
    )
    return [
        {"_id": str(d["_id"]), "name": d["name"], "slug": d["slug"]} for d in cursor
    ]


def get_publications_by_ids(db: Database, ids: List[str]) -> List[dict]:
    object_ids = []
    for s in ids:
        try:
            object_ids.append(ObjectId(s))
        except:
            continue

    cursor = db[PUBLICATION_COLLECTION].find(
        {"_id": {"$in": object_ids}},
        {"title": 1, "kind": 1, "keywords": 1},
    )
    pubs = []
    for p in cursor:
        pubs.append(
            {
                "_id": str(p["_id"]),
                "title": p.get("title"),
                "kind": p.get("kind"),
                "keywords": p.get("keywords", []),
            }
        )
    return pubs
