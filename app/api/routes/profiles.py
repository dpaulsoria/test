from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.profile import Profile
from app.models.job import Job
from app.schemas.profile import ProfileCreate, ProfileOut
from app.schemas.job import JobOut
from app.services.scoring import score_job

router = APIRouter(prefix="/profiles", tags=["profiles"])

def _split_csv(s: str) -> list[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]

@router.post("", response_model=ProfileOut)
def create_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    p = Profile(
        name=payload.name,
        role_focus=payload.role_focus,
        english_level=payload.english_level,
        keywords=",".join(payload.keywords),
        exclude_keywords=",".join(payload.exclude_keywords),
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return ProfileOut(
        id=p.id,
        name=p.name,
        role_focus=p.role_focus,
        english_level=p.english_level,
        keywords=_split_csv(p.keywords),
        exclude_keywords=_split_csv(p.exclude_keywords),
    )

@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    p = db.query(Profile).get(profile_id)
    if not p:
        raise HTTPException(404, "Profile not found")
    return ProfileOut(
        id=p.id,
        name=p.name,
        role_focus=p.role_focus,
        english_level=p.english_level,
        keywords=_split_csv(p.keywords),
        exclude_keywords=_split_csv(p.exclude_keywords),
    )

@router.get("/{profile_id}/matches")
def matches(
    profile_id: int,
    min_score: int = Query(50, ge=0, le=100),
    limit: int = Query(30, ge=1, le=200),
    db: Session = Depends(get_db),
):
    p = db.query(Profile).get(profile_id)
    if not p:
        raise HTTPException(404, "Profile not found")

    keywords = _split_csv(p.keywords)
    exclude = _split_csv(p.exclude_keywords)

    jobs = db.query(Job).order_by(Job.created_at.desc()).limit(500).all()
    scored = []
    for j in jobs:
        s = score_job(keywords, exclude, j.title, j.description)
        if s >= min_score:
            scored.append({"score": s, "job": JobOut.model_validate(j)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]
