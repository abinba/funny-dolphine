from pydantic import BaseModel

from src.schemas.chapter import ChapterFlat


class ChapterInfo(BaseModel):
    chapter: ChapterFlat
    listened_times: int


class UserAudiobookSchema(BaseModel):
    last_listened_chapter_id: int
    chapters: list[ChapterInfo]
