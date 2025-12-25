import feedparser
from sqlalchemy.orm import Session
from app.models.job import Job
from app.services.dedup import dedup_key

def ingest_rss(db: Session, url: str) -> int:
    feed = feedparser.parse(url)
    inserted = 0

    for e in feed.entries:
        title = getattr(e, "title", "") or ""
        link = getattr(e, "link", "") or ""
        if not link or not title:
            continue

        company = ""
        location = "Remote"
        desc = getattr(e, "summary", "") or getattr(e, "description", "") or ""

        key = dedup_key(title, company, location)

        # dedup por URL primero (más confiable)
        existing = db.query(Job).filter(Job.url == link).first()
        if existing:
            continue

        # dedup por key
        existing2 = db.query(Job).filter(Job.normalized_key == key).first()
        if existing2:
            continue

        job = Job(
            title=title[:200],
            company=company[:200],
            location=location[:200],
            url=link[:500],
            source=url[:200],
            description=desc,
            normalized_key=key,
            is_remote=True,
        )
        db.add(job)
        inserted += 1

    db.commit()
    return inserted
