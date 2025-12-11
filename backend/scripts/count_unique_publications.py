#!/usr/bin/env python3
import pandas as pd
import re

EXCEL_FILE = "project-dataset.xlsx"  # or correct path to your Excel file
SHEET_NAME = 0  # integer index or sheet name — use 0 or sheet name to get a DataFrame


def parse_publications_cell(raw):
    if pd.isna(raw):
        return []
    s = str(raw).strip()
    if not s:
        return []
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = s.split("\n")
    titles = []
    for line in lines:
        cleaned = re.sub(r"^\s*\d+\.\s*", "", line).strip()
        if cleaned:
            titles.append(cleaned)
    return titles


def main():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, engine="openpyxl")
    print(f"✅ Read DataFrame: {df.shape[0]} rows, {df.shape[1]} columns")

    all_titles = []
    for col in ["Article", "Conference Paper"]:
        if col not in df.columns:
            print(f"⚠️ Column '{col}' not found — skipping")
            continue
        for raw in df[col]:
            titles = parse_publications_cell(raw)
            all_titles.extend(titles)

    unique_titles = set(all_titles)
    print("📄 Total publication entries (including duplicates):", len(all_titles))
    print("🔖 Unique publication titles:", len(unique_titles))

    print("\n--- Sample unique titles (first 20) ---")
    for t in list(unique_titles)[:20]:
        print(" •", t)


if __name__ == "__main__":
    main()
