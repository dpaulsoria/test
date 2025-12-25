from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.config import settings
from app.services.ingest import ingest_rss

router = APIRouter(tags=["ingest"])

@router.post("/ingest")
def ingest(db: Session = Depends(get_db)):
    total = 0
    for src in settings.rss_sources:
        total += ingest_rss(db, src)
    return {"inserted": total, "sources": len(settings.rss_sources)}
