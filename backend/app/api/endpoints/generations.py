from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..models.models import EbookGeneration
from ..tasks.orchestration import run_ebook_orchestration
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/generations", tags=["generations"])

class GenerationCreate(BaseModel):
    topic_sentence: str
    config: Optional[dict] = None

@router.post("/")
async def create_generation(
    data: GenerationCreate,
    db: AsyncSession = Depends(get_db)
):
    # 1. Create DB entry
    new_gen = EbookGeneration(
        topic_sentence=data.topic_sentence,
        config_json=data.config,
        status="pending"
    )
    db.add(new_gen)
    await db.commit()
    await db.refresh(new_gen)
    
    # 2. Trigger Celery Task
    run_ebook_orchestration.delay(new_gen.id)
    
    return {"id": new_gen.id, "status": new_gen.status}

@router.get("/{gen_id}")
async def get_generation(
    gen_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(EbookGeneration).where(EbookGeneration.id == gen_id))
    gen = result.scalars().first()
    if not gen:
        raise HTTPException(status_code=404, detail="Generation not found")
    return gen
