from typing import List, Dict, Any, Optional
from pymongo.database import Database
from bson import ObjectId

PUBLICATION_COLLECTION = "publications"
FACULTY_COLLECTION = "faculties"


def get_all_publications(db: Database) -> List[Dict[str, Any]]:
    cursor = db[PUBLICATION_COLLECTION].find({})
    results = []
    for doc in cursor:
        pub_id = str(doc["_id"])
        authors = []
        for a in doc.get("authors", []):
            try:
                authors.append(ObjectId(a))
            except:
                pass

        faculty_cursor = db[FACULTY_COLLECTION].find(
            {"_id": {"$in": authors}},
            {"_id": 1, "name": 1, "position": 1},
        )

        author_list = [
            {"_id": str(f["_id"]), "name": f.get("name"), "position": f.get("position")}
            for f in faculty_cursor
        ]

        results.append(
            {
                "_id": pub_id,
                "title": doc.get("title"),
                "kind": doc.get("kind"),
                "keywords": doc.get("keywords", []),
                "authors": author_list,
            }
        )

    return results


def get_publication_by_id(db: Database, pub_id: str) -> Optional[Dict[str, Any]]:
    try:
        oid = ObjectId(pub_id)
    except Exception:
        return None

    doc = db[PUBLICATION_COLLECTION].find_one({"_id": oid})
    if not doc:
        return None

    authors = []
    for a in doc.get("authors", []):
        try:
            authors.append(ObjectId(a))
        except:
            pass

    faculty_cursor = db[FACULTY_COLLECTION].find(
        {"_id": {"$in": authors}},
        {"_id": 1, "name": 1, "position": 1},
    )

    author_list = [
        {"_id": str(f["_id"]), "name": f.get("name"), "position": f.get("position")}
        for f in faculty_cursor
    ]

    return {
        "_id": str(doc["_id"]),
        "title": doc.get("title"),
        "kind": doc.get("kind"),
        "keywords": doc.get("keywords", []),
        "authors": author_list,
    }
