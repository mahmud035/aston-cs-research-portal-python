#!/usr/bin/env python3
"""
Scan MongoDB `publications` collection for duplicates (same title + kind),
report how many duplicate groups and optionally delete duplicates (keep one per group).
"""

from pymongo import MongoClient, DeleteOne
from pprint import pprint

# === CONFIG ===
MONGO_URI = "mongodb://localhost:27017"  # or whatever your URI is
DB_NAME = "aston_cs_research_portal"  # your database name
COL_PUB = "publications"

# Set this to True if you want to delete duplicates (keep only one per title/kind)
DO_DELETE = True


def find_and_cleanup_duplicates():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    coll = db[COL_PUB]

    # 1. find duplicates grouped by title + kind
    pipeline = [
        {
            "$group": {
                "_id": {"title": "$title", "kind": "$kind"},
                "count": {"$sum": 1},
                "ids": {"$push": "$_id"},
            }
        },
        {"$match": {"count": {"$gt": 1}}},
    ]

    dupes = list(coll.aggregate(pipeline))
    total_groups = len(dupes)
    total_duplicates = sum(d["count"] - 1 for d in dupes)

    print("🔎 Found duplicate groups:", total_groups)
    print(
        "⚠️ Total extra duplicate documents (beyond first) that could be removed:",
        total_duplicates,
    )

    if total_groups == 0:
        print("✅ No duplicates. Nothing to do.")
    else:
        for entry in dupes:
            title = entry["_id"]["title"]
            kind = entry["_id"]["kind"]
            ids = entry["ids"]
            print(f"\nDuplicate group — title: {repr(title)}, kind: {kind}")
            print(" Document-IDs:", ids)

        if DO_DELETE:
            # build delete operations: for each group delete all except the first ID
            delete_ops = []
            for entry in dupes:
                ids = entry["ids"]
                # skip the first ID, delete the rest
                for dup_id in ids[1:]:
                    delete_ops.append(DeleteOne({"_id": dup_id}))

            if delete_ops:
                result = coll.bulk_write(delete_ops)
                print(f"\n🗑 Deleted {result.deleted_count} duplicate documents.")
            else:
                print("\nNo deletions needed (no extra docs beyond first).")

    client.close()


if __name__ == "__main__":
    find_and_cleanup_duplicates()
