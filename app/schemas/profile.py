from pydantic import BaseModel

class ProfileCreate(BaseModel):
    name: str
    role_focus: str = "backend"
    english_level: str = "B2"
    keywords: list[str] = []
    exclude_keywords: list[str] = []

class ProfileOut(BaseModel):
    id: int
    name: str
    role_focus: str
    english_level: str
    keywords: list[str]
    exclude_keywords: list[str]
