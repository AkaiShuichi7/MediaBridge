from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_openlist_data():
    return {"message": "Data from OpenList"}
