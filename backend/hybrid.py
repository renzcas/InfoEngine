from fastapi import FastAPI
from flask import Flask
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn

# --- FastAPI side ---
fastapi_app = FastAPI()

@fastapi_app.get("/hello_fastapi")
def hello_fastapi():
    return {"message": "Hello from FastAPI"}

# --- Flask side ---
flask_app = Flask(__name__)

@flask_app.route("/hello_flask")
def hello_flask():
    return {"message": "Hello from Flask"}

# --- Hybrid root ---
hybrid = FastAPI()

hybrid.mount("/flask", WSGIMiddleware(flask_app))
hybrid.mount("/api", fastapi_app)

if __name__ == "__main__":
    uvicorn.run(hybrid, host="0.0.0.0", port=5000)