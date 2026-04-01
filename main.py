from fastapi import FastAPI
from backend.organs import energy

app = FastAPI()

@app.get("/")
def home():
    return {"message": "InfoEngine is alive"}

@app.post("/organ/energy")
def run_energy(inputs: dict):
    return energy.run(inputs)