from typing import List, Dict, Any
from pymongo.database import Database
from bson import Regex, ObjectId

FACULTY_COLLECTION = "faculties"
PUBLICATION_COLLECTION = "publications"

def search_publications(db: Database, q: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Search publications by title or keywords (case-insensitive, partial match).
    """
    regex = Regex(f".*{q}.*", "i")  # case-insensitive regex
    cursor = db[PUBLICATION_COLLECTION].find({
        "$or": [
            { "title": { "$regex": regex } },
            { "keywords": { "$regex": regex } }
        ]
    }).skip(offset).limit(limit)

    results = []
    for doc in cursor:
        # minimal info or full depending on needs
        results.append({
            "_id": str(doc["_id"]),
            "title": doc.get("title"),
            "kind": doc.get("kind"),
            "keywords": doc.get("keywords", []),
            # optionally authors or skip to reduce payload
            "authorIds": [ str(a) for a in doc.get("authorIds", []) ]
        })
    return results

def search_faculties(db: Database, q: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Search faculties by name or researchInterest (partial, case-insensitive).
    """
    regex = Regex(f".*{q}.*", "i")
    cursor = db[FACULTY_COLLECTION].find({
        "$or": [
            { "name": { "$regex": regex } },
            { "researchInterest": { "$regex": regex } }
        ]
    }).skip(offset).limit(limit)

    results = []
    for doc in cursor:
        results.append({
            "_id": str(doc["_id"]),
            "name": doc.get("name"),
            "position": doc.get("position"),
            "researchInterest": doc.get("researchInterest"),
            "departmentIds": [ str(d) for d in doc.get("departmentIds", []) ]
        })
    return results
