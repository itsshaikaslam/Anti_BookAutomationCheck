from fastapi import FastAPI
from .core.database import engine, Base

app = FastAPI(title="Automated PDF Ebook Creation System")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Automatically create tables for now
        # In production, we should use Alembic
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "backend"}
