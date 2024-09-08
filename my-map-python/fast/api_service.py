from fastapi import APIRouter
from turkiye import data_turkiye

router = APIRouter()

@router.get("/api")
async def get_hello():
    mesaj = "Hello Deniz!"
    for i in range(1, 11):
        mesaj += str(i)
    return mesaj

@router.get('/api/harita')
async def get_harita():
    return data_turkiye

pass