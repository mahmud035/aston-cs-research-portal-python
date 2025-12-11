# api/index.py

from main import app as fastapi_app

# Vercel expects an `app` variable that is a WSGI/ASGI app
app = fastapi_app
