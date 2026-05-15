from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


class ToolCreate(ToolBase):
    pass


class Tool(ToolBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
