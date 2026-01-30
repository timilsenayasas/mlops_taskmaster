from fastapi import FastAPI, UploadFile, File
from worker import process_image_ml
import shutil
import os

app = FastAPI()

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Send to worker
    task = process_image_ml.delay(file_path)
    return {"task_id": task.id, "filename": file.filename}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)
    return {
        "status": task_result.status,
        "result": task_result.result
    }