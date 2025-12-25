from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.routes.ingest import router as ingest_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.profiles import router as profiles_router

# crea tablas (MVP). Luego puedes migrar a Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RemoteJob Radar")

app.include_router(ingest_router)
app.include_router(jobs_router)
app.include_router(profiles_router)

@app.get("/health")
def health():
    return {"ok": True}
