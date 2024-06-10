from celery import Celery
from database import genDatabase
from preprocess import PreprocessSteps
from config import Config

celery = Celery(
    "task", 
    backend = Config["redis_port"],
    broker = Config["redis_port"]
)

db = genDatabase()

@celery.task() 
def pipeline(id): 
    preprocess = PreprocessSteps()
    preprocess.extract_text_from_file(id)
    preprocess.text_cleanup_of_file(id)
    preprocess.triple_saver(id)
    return {"Success":f"Complete for {id}"}
