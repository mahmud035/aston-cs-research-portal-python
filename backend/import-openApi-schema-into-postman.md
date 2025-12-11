## How to import OpenAPI schema into Postman

## 📌 What the OpenAPI Schema URL Is

When your FastAPI server is running (e.g., with:

```bash
uvicorn main:app --reload
```

), it automatically exposes:

```
http://127.0.0.1:8000/openapi.json
```

This URL returns a JSON document that describes all your API endpoints, methods, parameters, request/response models, etc., in the **OpenAPI 3 format**.

Postman can import this and generate a full collection.

---

## 📥 Step-by-Step — Import OpenAPI into Postman

### 1. Start your FastAPI server

Make sure the backend is running:

```
uvicorn main:app --reload
```

and accessible at:

```
http://127.0.0.1:8000
```

### 2. Open Postman

Launch Postman.

### 3. Choose “Import”

In Postman’s top left, click:

```
Import
```

### 4. Select “Link” or “Import From Link”

In the Import modal, choose **Link**.

### 5. Paste the OpenAPI URL

Enter:

```
http://127.0.0.1:8000/openapi.json
```

Then click **Continue** → **Import**.

Postman will fetch that JSON and generate a complete collection for you, with all your `/api/v1/...` endpoints, parameters, example responses, etc.

---

## 🛠 Tips After Importing

✅ The imported collection will include:

- All your routes
- Path parameters
- Query parameters
- Request & response schemas

You can then:

- Run requests directly (e.g., `GET /departments`)
- Add environment variables (like `{{baseUrl}}`)
- Save example responses
- Create tests and workflows

---

## 📍 Example Retrofit

After importing, you might see endpoints like:

```
GET /api/v1/departments
GET /api/v1/departments/{slug}
GET /api/v1/faculties/{faculty_id}
GET /api/v1/publications
GET /api/v1/publications/{pub_id}
GET /api/v1/search
```

With those in place, click each one, set values for path parameters (e.g., a valid slug or ObjectId), and send requests.

---

## 🎯 Why This Is Useful

Importing OpenAPI into Postman gives you:

📌 A **ready-made API collection**
📌 Automatic parameter prompts
📌 Documentation-driven testing
📌 Ability to share with your team

---

## 🧪 Quick Troubleshooting

- If Postman can’t fetch the schema, check that:

  - Your server is running
  - You can open the URL in a browser

    ```
    http://127.0.0.1:8000/openapi.json
    ```

  - Postman’s network settings allow localhost requests
