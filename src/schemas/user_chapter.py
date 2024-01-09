from pydantic import BaseModel, ConfigDict


class UserChapterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    explored: bool
    listened_times: int
