from src.db.models import Account
from src.repo.base import BaseRepo
from src.schemas.account import AccountSchema
from src.schemas.account import AccountSchemaWithoutId


class AccountRepo(BaseRepo):
    model = Account
    validation_schema = AccountSchema


class AccountRepoWithoutId(BaseRepo):
    model = Account
    validation_schema = AccountSchemaWithoutId
