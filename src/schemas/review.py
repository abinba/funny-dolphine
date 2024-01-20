from pydantic import ConfigDict
from datetime import datetime

from src.schemas.base import SchemaBase


class ReviewSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    audiobook_id: int
    rating_value: int
    rating_date: datetime
    review_content: str
