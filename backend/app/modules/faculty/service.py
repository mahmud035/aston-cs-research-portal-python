from typing import Optional, List
from pymongo.database import Database
from bson import ObjectId

FACULTY_COLLECTION = "faculties"
DEPARTMENT_COLLECTION = "departments"
PUBLICATION_COLLECTION = "publications"

def get_faculty_by_id(db: Database, faculty_id: str) -> Optional[dict]:
    """
    Fetch a faculty document by its ID (string of ObjectId).
    """
    try:
        oid = ObjectId(faculty_id)
    except Exception:
        return None

    doc = db[FACULTY_COLLECTION].find_one({ "_id": oid })
    if not doc:
        return None

    # convert _id to str
    doc["_id"] = str(doc["_id"])
    # convert referenced ObjectIds to str if present
    for key in ("departmentIds", "articleIds", "conferencePaperIds"):
        if key in doc and isinstance(doc[key], list):
            doc[key] = [str(x) for x in doc[key]]
    return doc

def get_departments_by_ids(db: Database, ids: List[str]) -> List[dict]:
    """
    Fetch multiple departments by their string IDs.
    """
    object_ids = []
    for s in ids:
        try:
            object_ids.append(ObjectId(s))
        except:
            continue

    cursor = db[DEPARTMENT_COLLECTION].find(
        { "_id": { "$in": object_ids } },
        { "_id": 1, "name": 1, "slug": 1 }
    )
    depts = []
    for d in cursor:
        depts.append({
            "_id": str(d["_id"]),
            "name": d.get("name"),
            "slug": d.get("slug"),
        })
    return depts

def get_publications_by_ids(db: Database, ids: List[str]) -> List[dict]:
    """
    Fetch publications (articles or conference) by list of IDs.
    """
    object_ids = []
    for s in ids:
        try:
            object_ids.append(ObjectId(s))
        except:
            continue

    cursor = db[PUBLICATION_COLLECTION].find(
        { "_id": { "$in": object_ids } },
        { "_id": 1, "title": 1, "kind": 1, "keywords": 1 }
    )
    pubs = []
    for p in cursor:
        pubs.append({
            "_id": str(p["_id"]),
            "title": p.get("title"),
            "kind": p.get("kind"),
            "keywords": p.get("keywords", []),
        })
    return pubs
