from fastapi import APIRouter, FastAPI

from src.api.audiobook import router as audiobook_router

api_router = APIRouter()

api_router.include_router(audiobook_router, prefix="/audiobook", tags=["audiobook"])


def setup_routers(app: FastAPI):
    app.include_router(api_router)
