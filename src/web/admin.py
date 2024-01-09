import os

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from src.db import engine
from src.db.models import Audiobook, UserSettings, Account, Category, Chapter
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


class AudiobookView(ModelView):
    exclude_fields_from_create = ["created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]


class UserSettingsView(ModelView):
    exclude_fields_from_create = ["created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]


class AccountView(ModelView):
    exclude_fields_from_create = ["created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]


class CategoryView(ModelView):
    exclude_fields_from_create = ["created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]


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

    admin.add_view(ChapterView(Chapter))
    admin.add_view(AccountView(Account))
    admin.add_view(UserSettingsView(UserSettings, label="User Settings"))
    admin.add_view(CategoryView(Category, label="Categories"))
    admin.add_view(AudiobookView(Audiobook))

    admin.mount_to(app)
