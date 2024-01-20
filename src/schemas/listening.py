from pydantic import ConfigDict
from datetime import datetime

from src.schemas.base import SchemaBase


class ListeningSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    client_id: int
    audiobook_id: int
    current_chapter_id: int
    start_time: datetime
    last_access_time: datetime
    finish_time: datetime
    is_favorite: bool
