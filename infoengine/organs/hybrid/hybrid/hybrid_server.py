from fastapi import FastAPI
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn

# FastAPI side
fastapi_app = FastAPI()

@fastapi_app.get("/fastapi-heartbeat")
def fastapi_beat():
    return {"status": "fastapi alive"}

# Flask side
flask_app = Flask(__name__)

@flask_app.route("/flask-heartbeat")
def flask_beat():
    return {"status": "flask alive"}

# Hybrid mount
hybrid = FastAPI()
hybrid.mount("/flask", WSGIMiddleware(flask_app))
hybrid.mount("/api", fastapi_app)

if __name__ == "__main__":
    uvicorn.run(hybrid, host="0.0.0.0", port=5000)
