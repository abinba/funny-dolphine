from pydantic import ConfigDict

from src.schemas.base import SchemaBase


class UserSettingsSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    theme: str
    profile_picture: str
    language: str
    wifi_only: bool
    auto_play: bool
    notifications_enabled: bool
    adult_content_enabled: bool
    explicit_phrases: bool
