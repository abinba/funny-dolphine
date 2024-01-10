from src.db.models import UserChapter
from src.repo.base import BaseRepo
from src.schemas.user_chapter import UserChapterSchema


class UserChapterRepo(BaseRepo):
    model = UserChapter
    validation_schema = UserChapterSchema
