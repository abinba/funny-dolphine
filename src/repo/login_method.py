from src.db.models import LoginMethod
from src.repo.base import BaseRepo
from src.schemas.login_method import LoginMethodSchema


class LoginMethodRepo(BaseRepo):
    model = LoginMethod
    validation_schema = LoginMethodSchema
