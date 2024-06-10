from celery import Celery
from fastapi import File, UploadFile
from database import DatabaseControl

db = DatabaseControl()

celery = Celery(
    "task", 
    backend = "redis://localhost:6379",
    broker = "redis://localhost:6379" 
)

@celery.task() 
def pipeline(id): 
    db.extract_text_from_file(id)
    db.text_cleanup_of_file(id)
    db.triple_saver(id)
    return {"Success":f"Complete for {id}"}
