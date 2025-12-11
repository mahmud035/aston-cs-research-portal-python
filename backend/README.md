# 🧠 Aston CS Research Portal — Python Backend

## 📌 Overview

**Aston CS Research Portal** is a backend API built with **FastAPI** and **MongoDB** that exposes research data — departments, faculty profiles, and publications — in a structured, searchable format. It supports data import from an Excel sheet and provides endpoints to:

- List departments and related faculties
- Retrieve faculty profiles and their publications
- List publications and view individual publication details
- Search across research entities

This backend is designed to support both frontend applications and external clients via HTTP API.

---

## 🚀 What Does This Project Do?

- **Ingests research data** from an Excel file (`project-dataset.xlsx`)
- **Stores data** in a **MongoDB** database
- **Serves HTTP APIs** to:

  - Retrieve department and faculty data
  - Retrieve publication data
  - Perform keyword search

- Provides normalized responses for frontend consumption

---

## 🧠 How It Works

### 1. **Excel Import**

Your data is managed in an Excel spreadsheet with the following columns:

| Name | Position | Research Interest | Departmental Affiliation | Article | Conference Paper |
| ---- | -------- | ----------------- | ------------------------ | ------- | ---------------- |

The import process:

1. Parses every row of the spreadsheet
2. Normalizes & deduplicates:

   - Departments
   - Faculty members
   - Publication titles (articles & conference papers)

3. Extracts keywords from publication titles
4. Inserts documents in three MongoDB collections:

   - `departments`
   - `faculties`
   - `publications`

### 2. **API Layer**

A FastAPI application (`main.py`) serves routes under `/api/v1/` for:

- Departments
- Faculties
- Publications
- Search

Routes use **dependency injection** (`get_db`) to access the shared MongoDB connection.

Responses follow a **consistent JSON format** for status, messages, meta data, and the actual data.

---

## ✨ Core Features

### 🔹 Data Import

- Excel ingestion with Python
- Department split and matching to CS categories
- Deduplicated faculty and publication creation
- Keyword extraction

### 🔹 REST API

| Endpoint                         | Description                                                |
| -------------------------------- | ---------------------------------------------------------- |
| `GET /api/v1/departments`        | List all CS-related departments                            |
| `GET /api/v1/departments/{slug}` | Department details + all associated faculty                |
| `GET /api/v1/faculties/{id}`     | Full faculty profile, including departments & publications |
| `GET /api/v1/publications`       | List all publications                                      |
| `GET /api/v1/publications/{id}`  | Publication detail with authors                            |
| `GET /api/v1/search?q={keyword}` | Search across publications & faculty                       |

### 🔹 Backend Utilities

- Reusable database dependency (`get_db`)
- Consistent response format
- Pydantic schemas for structured responses
- Clean separation of controller, service, and schema layers

---

## 🏗️ Project Architecture

```
backend/
├── main.py                      # FastAPI entry point
├── app/
│   ├── core/
│   │   ├── db.py                # MongoDB connection & dependency
│   │   ├── utils.py             # Shared response helpers
│   │   ├── error_handlers.py    # Unified error handling
│   └── modules/
│       ├── department/
│       │   ├── controller.py
│       │   ├── service.py
│       │   └── schemas.py
│       ├── faculty/
│       │   ├── controller.py
│       │   ├── service.py
│       │   └── schemas.py
│       ├── publication/
│       │   ├── controller.py
│       │   ├── service.py
│       │   └── schemas.py
│       └── search/
│           ├── controller.py
│           └── service.py
├── scripts/
│   ├── import_excel.py          # Excel import script
│   ├── cleanup_duplicates.py    # Duplicate cleanup
│   └── count_unique_publications.py
├── project-dataset.xlsx         # Excel source data
├── requirements.txt
├── .env
```

---

## 🧩 Setup Guide

### ⚙️ Prerequisites

- Python 3.10+
- MongoDB running locally or remote (Atlas, etc.)
- `.env` file with:

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=aston_cs_research_portal
```

### 📦 1. Install Dependencies

Start your virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

### 📥 2. Import Data

```bash
python scripts/import_excel.py
```

Expected output:

- Departments created
- Faculty profiles inserted
- ~1294 publication documents

### 🚀 3. Run the API

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

### 📘 4. API Documentation (Swagger)

Visit:

```
http://127.0.0.1:8000/docs
```

This UI allows you to test all endpoints interactively.

---

## 📜 Postman API Documentation

You can test the APIs via Postman using the following basic collection or define your own based on the Swagger spec.

### Example Requests

| Name              | Method | URL                          |
| ----------------- | ------ | ---------------------------- |
| List Departments  | GET    | `/api/v1/departments`        |
| Get Department    | GET    | `/api/v1/departments/{slug}` |
| Get Faculty       | GET    | `/api/v1/faculties/{id}`     |
| List Publications | GET    | `/api/v1/publications`       |
| Search            | GET    | `/api/v1/search?q=keyword`   |

> 🚀 **Tip:** You can import the OpenAPI schema from `http://127.0.0.1:8000/openapi.json` directly into Postman.

---

## 🪪 Example Postman Environments

**Base URL:**

```
http://127.0.0.1:8000/api/v1
```

**Endpoints:**

```
GET {{baseUrl}}/departments
GET {{baseUrl}}/departments/school-of-...
GET {{baseUrl}}/faculties/693a...
GET {{baseUrl}}/publications
GET {{baseUrl}}/publications/693a...
GET {{baseUrl}}/search?q=artificial
```

---

## 🧠 Important Notes

- The backend uses **PyMongo** directly (not an ORM), giving full flexibility with MongoDB queries.
- All returned IDs are **stringified** (`str(ObjectId)`) to make them JSON friendly.
- Pydantic schemas ensure consistent API responses and docs.
- Search supports case-insensitive partial matching.

---

## 🧪 Testing Tips

- Use Swagger (`/docs`) for quick exploratory testing.
- Validate the total count of departments, faculty, and publications with Python REPL if needed.
- Use Postman variables to manage repeated IDs or base URLs.

---

## ❓ Frequently Asked

**Q: Why not use SQL?**
A: MongoDB’s flexible schema fits semi-structured publication and affiliation data.

**Q: Can we add pagination?**
A: Yes — endpoints can be extended with `limit` / `offset`.

**Q: How do I deploy?**
A: Deploy with a WSGI server like Uvicorn/Gunicorn; configure environment variables on hosts.

---

Feel free to ask if you want **Postman collections**, **Swagger export**, or **deployment instructions** (Docker/Heroku/AWS)!
