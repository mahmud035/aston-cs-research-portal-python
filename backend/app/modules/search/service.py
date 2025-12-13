from typing import List, Dict, Any
from pymongo.database import Database
from bson import ObjectId, Regex

FACULTY_COLLECTION = "faculties"
PUBLICATION_COLLECTION = "publications"


def search_publications(
    db: Database, q: str, limit: int = 20, offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Search publications by title or keywords and include authors details.
    """
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
        # stringify pub id
        pub_id = str(doc["_id"])

        # get authors field (may be list of ObjectIds or strings)
        raw_authors = doc.get("authors", [])  # match your store field name

        author_objs = []
        if raw_authors:
            # convert mixed types to ObjectId instances
            obj_ids = []
            for a in raw_authors:
                try:
                    obj_ids.append(ObjectId(a))
                except Exception:
                    continue

            # fetch faculty records for authors
            fac_cursor = db[FACULTY_COLLECTION].find(
                {"_id": {"$in": obj_ids}}, {"name": 1, "position": 1}
            )

            for f in fac_cursor:
                author_objs.append(
                    {
                        "_id": str(f["_id"]),
                        "name": f.get("name"),
                        "position": f.get("position"),
                    }
                )

        results.append(
            {
                "_id": pub_id,
                "title": doc.get("title"),
                "kind": doc.get("kind"),
                "keywords": doc.get("keywords", []),
                "authors": author_objs,
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
