import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .api.v1.api import api_router

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for request timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def startup():
    logger.info("Starting up server...")
    async with engine.begin() as conn:
        # In a real production app, use Alembic migrations instead of create_all
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables verified.")

@app.get("/health")
async def health_check():
    return {
        "status": "ok", 
        "timestamp": time.time(),
        "version": "1.0.0"
    }

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)
