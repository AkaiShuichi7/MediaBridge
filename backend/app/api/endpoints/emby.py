from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_emby_data():
    return {"message": "Data from Emby"}
