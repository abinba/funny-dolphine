import os

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from src.db import engine
from src.db.models import (
    Audiobook,
    UserSettings,
    Account,
    Category,
    Chapter,
    UserAudiobook,
    Review,
    Listening
)
from src.web.auth import ServiceAuthProvider


class ChapterView(ModelView):
    fields = [
        Chapter.chapter_id,
        Chapter.chapter_ordered_id,
        Chapter.audiobook,
        Chapter.parent,
        Chapter.sub_title,
        Chapter.full_text,
        Chapter.duration,
        Chapter.audio_file_url,
        "children",
    ]


def setup_admin(app: FastAPI):
    admin = Admin(
        engine,
        title="Funny Dolphine Admin",
        auth_provider=ServiceAuthProvider(),
        middlewares=[
            Middleware(
                SessionMiddleware,
                secret_key=os.environ.get("SESSION_SECRET_KEY")
            )
        ],
    )

    admin.add_view(ChapterView(Chapter))
    admin.add_view(ModelView(Account))
    admin.add_view(ModelView(UserSettings, label="User Settings"))
    admin.add_view(ModelView(Category, label="Categories"))
    admin.add_view(ModelView(Audiobook))
    admin.add_view(ModelView(UserAudiobook))
    admin.add_view(ModelView(Review))
    admin.add_view(ModelView(Listening))

    admin.mount_to(app)
