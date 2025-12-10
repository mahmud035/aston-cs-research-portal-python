from typing import List, Optional
from pymongo.database import Database
from bson import ObjectId

PUBLICATION_COLLECTION = "publications"
FACULTY_COLLECTION = "faculties"

def get_all_publications(db: Database) -> List[dict]:
    """
    Fetch all publications. Include authors (faculty) info joined by author IDs stored in publications.
    """
    cursor = db[PUBLICATION_COLLECTION].find({})
    results = []
    for doc in cursor:
        doc_id = str(doc["_id"])
        authors = []
        author_ids = doc.get("authorIds", [])
        if author_ids:
            # convert string/objectIds
            obj_ids = []
            for a in author_ids:
                try:
                    obj_ids.append(ObjectId(a))
                except:
                    continue
            authors_cursor = db[FACULTY_COLLECTION].find(
                { "_id": { "$in": obj_ids } },
                { "_id": 1, "name": 1, "position": 1 }
            )
            for a in authors_cursor:
                authors.append({
                    "_id": str(a["_id"]),
                    "name": a.get("name"),
                    "position": a.get("position")
                })

        results.append({
            "_id": doc_id,
            "title": doc.get("title"),
            "kind": doc.get("kind"),
            "keywords": doc.get("keywords", []),
            "authors": authors,
        })
    return results

def get_publication_by_id(db: Database, pub_id: str) -> Optional[dict]:
    """
    Fetch a single publication by its ID, including authors info.
    """
    try:
        oid = ObjectId(pub_id)
    except Exception:
        return None

    doc = db[PUBLICATION_COLLECTION].find_one({ "_id": oid })
    if not doc:
        return None

    authors = []
    author_ids = doc.get("authorIds", [])
    if author_ids:
        obj_ids = []
        for a in author_ids:
            try:
                obj_ids.append(ObjectId(a))
            except:
                continue
        authors_cursor = db[FACULTY_COLLECTION].find(
            { "_id": { "$in": obj_ids } },
            { "_id": 1, "name": 1, "position": 1 }
        )
        for a in authors_cursor:
            authors.append({
                "_sub_id": str(a["_id"]),
                "name": a.get("name"),
                "position": a.get("position")
            })

    return {
        "_id": str(doc["_id"]),
        "title": doc.get("title"),
        "kind": doc.get("kind"),
        "keywords": doc.get("keywords", []),
        "authors": authors,
    }
