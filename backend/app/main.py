from fastapi import FastAPI
from .core.database import engine, Base
from .api.endpoints import generations

app = FastAPI(title="Automated PDF Ebook Creation System")

# Include Routers
app.include_router(generations.router, prefix="/api")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Automatically create tables for now
        # In production, we should use Alembic
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "backend"}
