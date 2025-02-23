from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class HostBase(BaseModel):
    email: EmailStr
    host: str

class HostCreate(HostBase):
    pass

class HostResponse(HostBase):
    id: int
    is_up: bool
    last_check: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True