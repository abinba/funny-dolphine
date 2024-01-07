from pydantic import ConfigDict

from src.schemas.base import SchemaBase
from src.schemas.category import CategorySchema


class AudiobookSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    audiobook_id: int
    category_id: int
    title: str
    author: str
    description: str
    duration: int
    cover_image: str
    listened_times: int
    rating: float


class AudiobookWithCategorySchema(AudiobookSchema, CategorySchema):
    pass
