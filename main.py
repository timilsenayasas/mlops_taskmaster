from fastapi import FastAPI
from worker import simulate_ml_workload
from celery.result import AsyncResult

app = FastAPI(title="MLOps Taskmaster")

@app.post("/upload-data")
async def upload_data(name: str):
    # Trigger the Celery task (delay() runs it in background)
    task = simulate_ml_workload.delay(name)
    return {"task_id": task.id, "status": "Task Queued"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    # Check the status of the background task
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result if task_result.ready() else None
    }
    return result