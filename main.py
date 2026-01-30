from fastapi import FastAPI, UploadFile, File, HTTPException
from worker import process_image_ml
import shutil
import os

app = FastAPI(title="MLOps Taskmaster - Day 7 P2")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Day 13 Goal: Extension Validation
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG/JPG allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        task = process_image_ml.delay(file_path)
        return {"task_id": task.id, "filename": file.filename, "status": "Task Queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload: {str(e)}")

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }