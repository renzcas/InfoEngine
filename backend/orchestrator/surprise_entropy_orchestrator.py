from fastapi import APIRouter
import httpx

router = APIRouter()

# Adjust base URL if needed
BASE = "http://localhost:8000"

async def fetch_json(client, path):
    r = await client.get(f"{BASE}{path}")
    return r.json()

@router.get("/orchestrate/surprise_entropy")
async def orchestrate_surprise_entropy():
    async with httpx.AsyncClient() as client:
        system_state = await fetch_json(client, "/organ/mind/systemofsystems/global_state")
        heat_state = await fetch_json(client, "/organ/physics/environment_heat/heat_state/last")
        self_state = await fetch_json(client, "/organ/mind/self_reference/self_state/last")

        payload = {
            "system_state": system_state,
            "heat_state": heat_state,
            "self_state": self_state,
        }

        r = await client.post(
            f"{BASE}/organ/mind/surprise_entropy/state",
            json=payload
        )
        return r.json()
