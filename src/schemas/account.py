from pydantic import ConfigDict

from src.schemas.base import SchemaBase


class AccountSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    username: str
    is_active: bool
