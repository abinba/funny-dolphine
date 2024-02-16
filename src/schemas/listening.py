from pydantic import ConfigDict

from src.schemas.base import SchemaBase


class ListeningSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    audiobook_id: int
    current_chapter_id: int
