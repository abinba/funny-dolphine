from fastapi import FastAPI
from sqladmin import ModelView, Admin

from src.db import engine
from src.db.models import (
    Audiobook,
    UserSettings,
    Account,
    Category,
    Chapter,
    UserAudiobook,
    Review,
    Listening,
)


class ChapterView(ModelView, model=Chapter):
    column_list = [
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


class AccountView(ModelView, model=Account):
    column_list = [
        Account.account_id,
        Account.username,
        Account.is_active,
        Account.created_at,
        Account.updated_at,
    ]


class UserSettingsView(ModelView, model=UserSettings):
    column_list = [
        UserSettings.account_id,
        UserSettings.theme,
        UserSettings.profile_picture,
        UserSettings.language,
        UserSettings.wifi_only,
        UserSettings.auto_play,
        UserSettings.notifications_enabled,
        UserSettings.adult_content_enabled,
        UserSettings.explicit_phrases,
        UserSettings.created_at,
        UserSettings.updated_at,
    ]


class CategoryView(ModelView, model=Category):
    column_list = [
        Category.category_id,
        Category.name,
        Category.created_at,
        Category.updated_at,
    ]


class AudiobookView(ModelView, model=Audiobook):
    column_list = [
        Audiobook.audiobook_id,
        Audiobook.category_id,
        Audiobook.title,
        Audiobook.author,
        Audiobook.description,
        Audiobook.duration,
        Audiobook.cover_image,
        Audiobook.listened_times,
        Audiobook.rating,
        Audiobook.created_at,
        Audiobook.updated_at,
    ]


class UserAudiobookView(ModelView, model=UserAudiobook):
    column_list = [
        UserAudiobook.user_audiobook_id,
        UserAudiobook.account_id,
        UserAudiobook.audiobook_id,
        UserAudiobook.last_listened_chapter_id,
        UserAudiobook.created_at,
        UserAudiobook.updated_at,
    ]


class ReviewView(ModelView, model=Review):
    column_list = [
        Review.account_id,
        Review.audiobook_id,
        Review.rating_value,
        Review.rating_date,
        Review.review_content,
        Review.created_at,
        Review.updated_at,
    ]


class ListeningView(ModelView, model=Listening):
    column_list = [
        Listening.account_id,
        Listening.audiobook_id,
        Listening.current_chapter_id,
        Listening.start_time,
        Listening.last_access_time,
        Listening.finish_time,
        Listening.is_favorite,
        Listening.created_at,
        Listening.updated_at,
    ]


def setup_admin(app: FastAPI):
    admin = Admin(
        app,
        engine,
    )

    admin.add_view(ChapterView)
    admin.add_view(AccountView)
    admin.add_view(UserSettingsView)
    admin.add_view(CategoryView)
    admin.add_view(AudiobookView)
    admin.add_view(UserAudiobookView)
    admin.add_view(ReviewView)
    admin.add_view(ListeningView)
