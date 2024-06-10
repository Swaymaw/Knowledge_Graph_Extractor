from celery import Celery
from database import genDatabase
from preprocess import PreprocessSteps

celery = Celery(
    "task", 
    backend = "redis://localhost:6379",
    broker = "redis://localhost:6379" 
)

db = genDatabase()

@celery.task() 
def pipeline(id): 
    preprocess = PreprocessSteps()
    preprocess.extract_text_from_file(id)
    preprocess.text_cleanup_of_file(id)
    preprocess.triple_saver(id)
    return {"Success":f"Complete for {id}"}
