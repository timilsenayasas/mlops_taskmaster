import os
import logging
from celery import Celery
from PIL import Image, ImageOps

# Setup professional logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery(
    "ml_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_image_ml(self, file_path: str):
    try:
        logger.info(f"Processing task started for: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")

        with Image.open(file_path) as img:
            # Simulate ML transformation
            processed_img = ImageOps.grayscale(img)
            
            output_path = file_path.replace("uploads/", "uploads/processed_")
            processed_img.save(output_path)
            
        logger.info(f"Task successful. Output saved to: {output_path}")
        return {"status": "Success", "output_file": output_path}

    except Exception as exc:
        logger.error(f"Task failed for {file_path}: {exc}")
        # Automatically retries based on autoretry_for
        raise exc