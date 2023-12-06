from fastapi import FastAPI

from src.api import setup_routers


def create_app() -> FastAPI:
    _app = FastAPI()

    setup_routers(_app)

    return _app
