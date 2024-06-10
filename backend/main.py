from fastapi import FastAPI, UploadFile, File
from database import genDatabase
from task import pipeline
from fastapi.middleware.cors import CORSMiddleware
from config import Config

app = FastAPI()

origins = [
    Config.origin
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = genDatabase()

@app.get("/")
async def get_root():
    return {"File": "Upload"}

@app.post("/uploadfile")
async def create_file(file: UploadFile = File(...)):
    response = db.save_file_content(file)
    return response

@app.put("/fullpipeline")
async def complete_pipeline(file_id):
    job_id = pipeline.delay(file_id) 
    job_id = str(job_id)
    db.jobid_update(file_id, job_id)
    return {"job_id": job_id}

@app.get("/gettriplets")
async def get_triplet_dict(file_id):
    response = db.find_triplets(file_id)
    return response

@app.get("/getprogress")
async def document_progress(file_id):
    response = db.find_progress(file_id)
    return response

@app.get("/getall")
async def get_all_data():
    response = db.fetch_all_data()
    return response

@app.delete("/delete_file")
async def delete_file_by_name(file_id): 
    response = db.delete_file(file_id)
    return response

@app.delete("/reset_db")
async def clear_database():
    response = db.clear_db()
    return response
