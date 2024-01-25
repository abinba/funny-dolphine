from pydantic import ConfigDict
from src.schemas.base import SchemaBase


class SaltSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    salt: str
