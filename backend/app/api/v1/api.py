from fastapi import APIRouter
from .endpoints import generations

api_router = APIRouter()
api_router.include_router(generations.router, prefix="/generations", tags=["generations"])
