from fastapi import FastAPI

from src.api import setup_routers
from src.web.admin import setup_admin


def create_app() -> FastAPI:
    _app = FastAPI()

    setup_routers(_app)
    setup_admin(_app)

    return _app
