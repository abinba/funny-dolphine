import os

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from src.db import engine
from src.db.models import Audiobook, UserSettings, Account, Category
from src.web.auth import ServiceAuthProvider


def setup_admin(app: FastAPI):
    admin = Admin(
        engine,
        title="Funny Dolphine Admin",
        auth_provider=ServiceAuthProvider(),
        middlewares=[
            Middleware(
                SessionMiddleware, secret_key=os.environ.get("SESSION_SECRET_KEY")
            )
        ],
    )

    admin.add_view(ModelView(Account))
    admin.add_view(ModelView(UserSettings, label="User Settings"))
    admin.add_view(ModelView(Category, label="Categories"))
    admin.add_view(ModelView(Audiobook))

    admin.mount_to(app)
