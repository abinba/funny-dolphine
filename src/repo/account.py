from src.db.models import Account
from src.repo.base import BaseRepo
from src.schemas.account import AccountSchema


class AccountRepo(BaseRepo):
    model = Account
    validation_schema = AccountSchema
