from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  #  check validation for pending/completed later

    @field_validator("status")
    def check_status(cls, v):
        if v is not None and v not in ("pending", "completed"):
            raise ValueError("Status must be 'pending' or 'completed'")
        return v

class TodoOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
