from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class GenerationBase(BaseModel):
    topic_sentence: str = Field(..., example="The future of renewable energy in 2050")
    config_json: Optional[Dict[str, Any]] = None

class GenerationCreate(GenerationBase):
    pass

class GenerationUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[int] = None
    pdf_link: Optional[str] = None
    gdrive_link: Optional[str] = None

class GenerationRead(GenerationBase):
    id: int
    status: str
    progress: int
    current_agent: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
