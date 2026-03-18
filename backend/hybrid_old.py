from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from flask_app import flask_app
from api import fastapi_app

app = FastAPI(title="InfoEngine Hybrid Backend")

# Mount Flask at root
app.mount("/", WSGIMiddleware(flask_app))

# Mount FastAPI under /api
app.mount("/api", fastapi_app)
