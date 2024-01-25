from src.db.models import Salt
from src.repo.base import BaseRepo
from src.schemas.salt import SaltSchema


class SaltRepo(BaseRepo):
    model = Salt
    validation_schema = SaltSchema
