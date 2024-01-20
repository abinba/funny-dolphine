from src.db.models import Listening
from src.repo.base import BaseRepo
from src.schemas.listening import ListeningSchema


class ListeningRepo(BaseRepo):
    model = Listening
    validation_schema = ListeningSchema
