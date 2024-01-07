from datetime import datetime

from pydantic import BaseModel


class SchemaBase(BaseModel):
    created_at: datetime
    updated_at: datetime
