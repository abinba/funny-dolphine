from src.db.models import UserSettings
from src.repo.base import BaseRepo


class UserSettingsRepo(BaseRepo):
    model = UserSettings
