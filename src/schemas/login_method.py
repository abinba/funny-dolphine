from pydantic import ConfigDict
from src.schemas.base import SchemaBase


class LoginMethodSchema(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    login_email: str
    login_password: str
