from fastapi import APIRouter

router = APIRouter()

@router.get("/panels")
def panels():
    return {"panels": ["cyber", "physics", "mind", "hybrid"]}
