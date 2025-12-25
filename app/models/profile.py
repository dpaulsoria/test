from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    role_focus: Mapped[str] = mapped_column(String(120), default="backend")
    english_level: Mapped[str] = mapped_column(String(20), default="B2")
    keywords: Mapped[str] = mapped_column(String(1000), default="")  # CSV: "python,fastapi,postgres"
    exclude_keywords: Mapped[str] = mapped_column(String(1000), default="")  # CSV
