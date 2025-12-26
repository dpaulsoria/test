from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.db.session import engine
from app.db.base import Base
from app.api.routes.ingest import router as ingest_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.profiles import router as profiles_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RemoteJob Radar")

app.include_router(ingest_router)
app.include_router(jobs_router)
app.include_router(profiles_router)

WEB_DIR = Path(__file__).parent / "web"

app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

@app.get("/")
def web_index():
    return FileResponse(WEB_DIR / "index.html")

@app.get("/health")
def health():
    return {"ok": True}
