import os
from celery import Celery
from PIL import Image, ImageOps

celery_app = Celery(
    "ml_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def process_image_ml(file_path: str):
    # Simulate ML processing (Grayscale filter)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    img = Image.open(file_path)
    processed_img = ImageOps.grayscale(img)
    
    # Save the "result"
    output_path = file_path.replace("uploads/", "uploads/processed_")
    processed_img.save(output_path)
    
    return {"status": "Success", "output_file": output_path}