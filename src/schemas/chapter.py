from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChapterBase(BaseModel):
    chapter_id: int
    chapter_ordered_id: int
    audiobook_id: int
    parent_id: Optional[int]
    sub_title: str
    full_text: str
    duration: int
    audio_file_url: str


class ChapterTree(ChapterBase):
    model_config = ConfigDict(from_attributes=True)

    children: Optional[list["ChapterTree"]]


class ChapterFlat(ChapterBase):
    model_config = ConfigDict(from_attributes=True)

    children_ids: Optional[list[int]]
