import time
from celery import Celery

# Setup Celery to use Redis as the broker and backend
celery_app = Celery(
    "ml_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task(bind=True)
def simulate_ml_workload(self, data_name: str):
    print(f"Starting heavy ML processing for: {data_name}")
    
    # Simulate an ML model loading and processing (10 seconds)
    for i in range(10):
        time.sleep(1)
        # Update progress (optional)
        self.update_state(state='PROGRESS', meta={'current': i+1, 'total': 10})
    
    print(f"Finished processing: {data_name}")
    return {"status": "Success", "result": f"Model results for {data_name} are ready."}