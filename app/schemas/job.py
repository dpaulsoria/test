from pydantic import BaseModel
from datetime import datetime

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    url: str
    source: str
    description: str
    is_remote: bool
    created_at: datetime

    class Config:
        from_attributes = True
