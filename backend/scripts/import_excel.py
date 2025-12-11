#!/usr/bin/env python3
"""
import_excel.py

Reads Excel spreadsheet (with columns: Name, Position, Research Interest,
Departmental Affiliation, Article, Conference Paper), and imports data into
MongoDB using PyMongo — creating Department, Faculty, and Publication documents.

Mirrors the logic of your original importFromExcel.ts, with added safety for empty cells.
"""

import os
import re
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Config — adjust as needed
MONGO_URI = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "aston_cs_research_portal")

# Excel file — change path if needed
EXCEL_FILE = "project-dataset.xlsx"

# Collections
COL_DEPT = "departments"
COL_FAC = "faculties"
COL_PUB = "publications"

# STOP words for keyword extraction
STOP_WORDS = set(
    [
        "a",
        "an",
        "the",
        "in",
        "on",
        "of",
        "for",
        "and",
        "or",
        "to",
        "with",
        "by",
        "from",
        "at",
        "as",
        "into",
        "about",
        "over",
        "under",
        "between",
        "through",
        "without",
        "within",
        "across",
        "is",
        "are",
        "be",
        "this",
        "that",
        "these",
        "those",
        "overview",
    ]
)


def slugify(value: str) -> str:
    """
    Simplified slugify: remove non-alphanum, spaces → hyphens, lowercase.
    """
    s = value.strip().lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def extract_keywords_from_title(title: str) -> List[str]:
    """
    Split by non-alphanumeric, lowercase, filter stop words + short tokens.
    """
    cleaned = re.sub(r"[^a-z0-9]+", " ", title.lower())
    tokens = [t for t in cleaned.split() if t and t not in STOP_WORDS and len(t) > 2]
    seen = set()
    result = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result


def parse_departments(raw: str) -> List[str]:
    """
    Split Departmental Affiliation by newline or comma, dedupe, trim.
    """
    parts = []
    for line in re.split(r"\r?\n", raw):
        for sub in line.split(","):
            s = sub.strip()
            if s:
                parts.append(s)
    # dedupe preserving order
    seen = set()
    result = []
    for s in parts:
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result


def parse_publication_titles(raw: str) -> List[str]:
    """
    Parse Article / Conference Paper field containing possibly multiple titles,
    separated by newline, maybe numbered (e.g. "1. Title\n2. Title").
    """
    normalized = raw.replace("\r\n", "\n").strip()
    if not normalized:
        return []
    lines = normalized.split("\n")
    titles = []
    for line in lines:
        cleaned = re.sub(r"^\s*\d+\.\s*", "", line).strip()
        if cleaned:
            titles.append(cleaned)
    return titles


def is_cs_department(name: str) -> bool:
    """
    Rough heuristic to detect if department is CS-related.
    """
    lower = name.lower()
    keywords = [
        "computer science",
        "software engineering",
        "cybersecurity",
        "cyber security",
        "artificial intelligence",
        "applied ai",
        "ai & robotics",
        "data science",
        "computer science research group",
        "software engineering & cybersecurity",
        "ai robotics",
    ]
    for kw in keywords:
        if kw in lower:
            return True
    return False


def detect_department_type(name: str) -> str:
    lower = name.lower()
    if "school" in lower:
        return "school"
    if "centre" in lower or "center" in lower:
        return "centre"
    if "group" in lower:
        return "group"
    if "college" in lower:
        return "college"
    return "other"


def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print("✅ Connected to MongoDB:", DB_NAME)

    # Read Excel — force all columns as string, fill NaN with empty strings
    df = pd.read_excel(EXCEL_FILE, engine="openpyxl", dtype=str)
    df = df.fillna("")  # replace NaN with empty string
    print(f"📄 Read {len(df)} rows from Excel")

    # Optional: clear existing collections
    db[COL_DEPT].delete_many({})
    db[COL_FAC].delete_many({})
    db[COL_PUB].delete_many({})
    print("🧹 Cleared Department, Faculty, Publication collections")

    dept_cache: dict[str, ObjectId] = {}
    pub_cache: dict[tuple[str, str], ObjectId] = {}

    for idx, row in df.iterrows():
        name = row.get("Name", "").strip()
        if not name:
            print(f"⚠️ Row {idx+2}: no Name — skipping")
            continue

        position = row.get("Position", "").strip() or None
        research_interest = row.get("Research Interest", "").strip() or None
        raw_dept = row.get("Departmental Affiliation", "").strip() or ""
        article_raw = row.get("Article", "")
        conf_raw = row.get("Conference Paper", "")

        # 1. Departments
        dept_names = parse_departments(raw_dept)
        dept_ids = []
        for dn in dept_names:
            if not is_cs_department(dn):
                continue
            if dn not in dept_cache:
                slug = slugify(dn)
                dept_doc = {
                    "name": dn,
                    "slug": slug,
                    "type": detect_department_type(dn),
                    "description": None,
                    "isComputerScienceRelated": True,
                }
                res = db[COL_DEPT].insert_one(dept_doc)
                dept_id = res.inserted_id
                dept_cache[dn] = dept_id
                print("➕ Created CS department:", dn)
            else:
                dept_id = dept_cache[dn]
            dept_ids.append(dept_id)

        # 2. Faculty
        fac_doc = {
            "name": name,
            "position": position,
            "researchInterest": research_interest,
            "rawDepartmentAffiliation": raw_dept,
            "departmentIds": dept_ids,
            "articleIds": [],
            "conferencePaperIds": [],
        }
        fac_res = db[COL_FAC].insert_one(fac_doc)
        faculty_id = fac_res.inserted_id
        print("👤 Created faculty:", name)

        # 3. Articles
        article_titles = parse_publication_titles(article_raw or "")
        for title in article_titles:
            key = ("article", title)
            if key not in pub_cache:
                pub_doc = {
                    "title": title,
                    "kind": "article",
                    "authors": [faculty_id],
                    "keywords": extract_keywords_from_title(title),
                    "source": {"excelColumn": "Article", "excelRowIndex": int(idx)},
                }
                res = db[COL_PUB].insert_one(pub_doc)
                pub_id = res.inserted_id
                pub_cache[key] = pub_id
                print("📄 Created article:", title)
            else:
                pub_id = pub_cache[key]
                db[COL_PUB].update_one(
                    {"_id": pub_id, "authors": {"$ne": faculty_id}},
                    {"$push": {"authors": faculty_id}},
                )
            db[COL_FAC].update_one(
                {"_id": faculty_id}, {"$push": {"articleIds": pub_id}}
            )

        # 4. Conference Papers
        conf_titles = parse_publication_titles(conf_raw or "")
        for title in conf_titles:
            key = ("conference", title)
            if key not in pub_cache:
                pub_doc = {
                    "title": title,
                    "kind": "conference",
                    "authors": [faculty_id],
                    "keywords": extract_keywords_from_title(title),
                    "source": {
                        "excelColumn": "Conference Paper",
                        "excelRowIndex": int(idx),
                    },
                }
                res = db[COL_PUB].insert_one(pub_doc)
                pub_id = res.inserted_id
                pub_cache[key] = pub_id
                print("🎤 Created conference paper:", title)
            else:
                pub_id = pub_cache[key]
                db[COL_PUB].update_one(
                    {"_id": pub_id, "authors": {"$ne": faculty_id}},
                    {"$push": {"authors": faculty_id}},
                )
            db[COL_FAC].update_one(
                {"_id": faculty_id}, {"$push": {"conferencePaperIds": pub_id}}
            )

    print("✅ Import completed.")
    client.close()
    print("🔌 Disconnected from MongoDB")


if __name__ == "__main__":
    main()
