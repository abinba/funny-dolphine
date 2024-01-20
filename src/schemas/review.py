from pydantic import ConfigDict
from datetime import datetime
from typing import Literal

from src.schemas.base import SchemaBase


class ReviewSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    client_id: int
    audiobook_id: int
    rating_value: Literal[1, 2, 3, 4, 5]
    rating_date: datetime
    review_content: str
