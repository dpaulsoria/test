from sqlalchemy import String, Text, DateTime, Integer, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    company: Mapped[str] = mapped_column(String(200), default="")
    location: Mapped[str] = mapped_column(String(200), default="Remote")
    url: Mapped[str] = mapped_column(String(500), unique=True)
    source: Mapped[str] = mapped_column(String(200), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    normalized_key: Mapped[str] = mapped_column(String(64), index=True)  # dedup key
    is_remote: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

Index("ix_jobs_normkey", Job.normalized_key)
