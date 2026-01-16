from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...core.database import get_db
from ...models.models import EbookGeneration
from ...schemas.generation import GenerationCreate, GenerationRead
from ...tasks.orchestration import run_ebook_orchestration

router = APIRouter()

@router.post("/", response_model=GenerationRead, status_code=status.HTTP_201_CREATED)
async def create_generation(
    *,
    db: AsyncSession = Depends(get_db),
    generation_in: GenerationCreate
) -> Any:
    """
    Initiate a new ebook generation process.
    """
    new_gen = EbookGeneration(
        topic_sentence=generation_in.topic_sentence,
        config_json=generation_in.config_json,
        status="pending"
    )
    db.add(new_gen)
    await db.flush()  # Get the ID before commit
    
    # Trigger the background orchestration task
    run_ebook_orchestration.delay(new_gen.id)
    
    return new_gen

@router.get("/", response_model=List[GenerationRead])
async def read_generations(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all generation tasks for the current user.
    """
    result = await db.execute(select(EbookGeneration).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{gen_id}", response_model=GenerationRead)
async def read_generation_by_id(
    gen_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get detailed status of a specific generation task.
    """
    result = await db.execute(select(EbookGeneration).where(EbookGeneration.id == gen_id))
    gen = result.scalars().first()
    if not gen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generation task not found"
        )
    return gen
