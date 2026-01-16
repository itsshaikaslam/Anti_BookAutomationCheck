import logging
import time
from celery import shared_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
from ..models.models import EbookGeneration

logger = logging.getLogger(__name__)

# Synchronous engine for Celery tasks (easier for most workers)
sync_engine = create_engine(settings.sync_database_url)
SessionLocal = sessionmaker(bind=sync_engine)

@shared_task(bind=True, name="run_ebook_orchestration")
def run_ebook_orchestration(self, generation_id: int):
    """
    Main entry point for the 13-agent orchestration pipeline.
    """
    db = SessionLocal()
    try:
        gen = db.query(EbookGeneration).filter(EbookGeneration.id == generation_id).first()
        if not gen:
            logger.error(f"Generation {generation_id} not found in database.")
            return {"error": "not_found"}

        logger.info(f"Starting orchestration for task {generation_id}: {gen.topic_sentence}")
        
        gen.status = "processing"
        db.commit()

        agents = [
            "ConfigurationLoader", "TopicAnalysis", "ContentStrategy",
            "ResearchSwarm", "ChapterGeneration", "InfographicGeneration",
            "VisualDesign", "QualityEnhancement", "CriticProofreading",
            "SEOMetadata", "LayoutFormatting", "PDFGeneration", "StorageIntegration"
        ]
        
        for i, agent in enumerate(agents):
            progress = int((i + 1) / len(agents) * 100)
            logger.info(f"Task {generation_id} | Agent: {agent} | Progress: {progress}%")
            
            # Update DB
            gen.current_agent = agent
            gen.progress = progress
            db.commit()
            
            # Celery status update
            self.update_state(state='PROGRESS', meta={'agent': agent, 'progress': progress})
            
            # Simulate intense AI work
            time.sleep(2)
            
        gen.status = "completed"
        gen.completed_at = gen.started_at # Approximation for now
        db.commit()
        
        logger.info(f"Successfully completed task {generation_id}")
        return {"status": "completed", "generation_id": generation_id}

    except Exception as e:
        logger.exception(f"Critical failure in orchestration for task {generation_id}")
        if 'gen' in locals():
            gen.status = "failed"
            db.commit()
        return {"status": "failed", "error": str(e)}
    finally:
        db.close()
