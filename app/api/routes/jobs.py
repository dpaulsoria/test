from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.job import Job
from app.schemas.job import JobOut

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("", response_model=list[JobOut])
def list_jobs(
    q: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Job).order_by(Job.created_at.desc())
    if q:
        query = query.filter(Job.title.ilike(f"%{q}%"))
    return query.limit(limit).all()
