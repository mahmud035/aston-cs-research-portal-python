from typing import List, Dict, Any
from pymongo.database import Database
from bson import Regex

FACULTY_COLLECTION = "faculties"
PUBLICATION_COLLECTION = "publications"


def search_publications(
    db: Database, q: str, limit: int = 20, offset: int = 0
) -> List[Dict[str, Any]]:
    query_regex = Regex(f".*{q}.*", "i")
    cursor = (
        db[PUBLICATION_COLLECTION]
        .find(
            {
                "$or": [
                    {"title": {"$regex": query_regex}},
                    {"keywords": {"$regex": query_regex}},
                ]
            }
        )
        .skip(offset)
        .limit(limit)
    )

    results = []
    for doc in cursor:
        results.append(
            {
                "_id": str(doc["_id"]),
                "title": doc.get("title"),
                "kind": doc.get("kind"),
                "keywords": doc.get("keywords", []),
            }
        )
    return results


def search_faculties(
    db: Database, q: str, limit: int = 20, offset: int = 0
) -> List[Dict[str, Any]]:
    query_regex = Regex(f".*{q}.*", "i")
    cursor = (
        db[FACULTY_COLLECTION]
        .find(
            {
                "$or": [
                    {"name": {"$regex": query_regex}},
                    {"researchInterest": {"$regex": query_regex}},
                ]
            }
        )
        .skip(offset)
        .limit(limit)
    )

    results = []
    for doc in cursor:
        results.append(
            {
                "_id": str(doc["_id"]),
                "name": doc.get("name"),
                "position": doc.get("position"),
                "researchInterest": doc.get("researchInterest"),
            }
        )
    return results
