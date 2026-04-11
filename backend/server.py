# backend/server.py

import asyncio
import json
from fastapi import FastAPI, WebSocket
from core.system import OrganismSystem

app = FastAPI()
system = OrganismSystem()

@app.websocket("/cockpit")
async def cockpit_ws(ws: WebSocket):
    await ws.accept()

    t = 0.0
    dt = 0.5

    while True:
        # Example input
        inputs = [{"type": "packet", "source_id": "agent_1", "event": "scan"}]

        snapshot = system.step(dt, inputs)
        snapshot["timestamp"] = t

        await ws.send_text(json.dumps(snapshot))

        await asyncio.sleep(dt)
        t += dt
