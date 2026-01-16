from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EbookGeneration(Base):
    __tablename__ = "ebook_generations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_sentence = Column(Text, nullable=False)
    config_json = Column(JSON, nullable=True)
    status = Column(String(20), default="pending")
    progress = Column(Integer, default=0)
    current_agent = Column(String(50), nullable=True)
    pdf_link = Column(Text, nullable=True)
    gdrive_link = Column(Text, nullable=True)
    fact_accuracy_score = Column(Float, nullable=True)
    readability_score = Column(Float, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(Integer, ForeignKey("ebook_generations.id"))
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    depth_level = Column(Integer, default=0)
    content_markdown = Column(Text, nullable=True)
    word_count = Column(Integer, default=0)
    status = Column(String(20), default="drafting")
    infographic_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FactVerification(Base):
    __tablename__ = "fact_verifications"
    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(Integer, ForeignKey("ebook_generations.id"))
    claim_text = Column(Text, nullable=False)
    verified = Column(Boolean, default=False)
    confidence_score = Column(Float, nullable=True)
    source = Column(Text, nullable=True)

class AgentLog(Base):
    __tablename__ = "agent_logs"
    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(Integer, ForeignKey("ebook_generations.id"))
    agent_name = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    execution_time = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)

class Infographic(Base):
    __tablename__ = "infographics"
    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(Integer, ForeignKey("ebook_generations.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    chapter_number = Column(Integer, nullable=False)
    minio_path = Column(Text, nullable=False)
    image_type = Column(String(50), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
