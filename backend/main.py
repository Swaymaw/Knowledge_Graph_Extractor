from fastapi import FastAPI, UploadFile, File
from database import DatabaseControl
from task import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DatabaseControl()

@app.get("/")
def get_root():
    return {"File": "Upload"}

@app.post("/uploadfile")
async def create_file(file: UploadFile = File(...)):
    response = db.save_file_content(file)
    return response

@app.put("/fullpipeline")
def complete_pipeline(file_id):
    job_id = pipeline.delay(file_id) 
    job_id = str(job_id)
    db.jobid_update(file_id, job_id)
    return {"job_id": job_id}

@app.put("/extracttext")
def extract_text(file_id):
    response = db.extract_text_from_file(file_id)
    print(response)
    return {"details": response}

@app.put("/cleantext")
def cleanup_text(file_id):
    response = db.text_cleanup_of_file(file_id)
    return response

@app.put("/tripletsgen")
def gen_triplets(file_id):
    response = db.triple_saver(file_id)
    return response

@app.get("/filecontent")
def get_file_text(file_id):
    response = db.find_file(file_id)
    return response

@app.get("/gettriplets")
def get_triplet_dict(file_id):
    response = db.find_triplets(file_id)
    return response

@app.get("/getprogress")
def document_progress(file_id):
    response = db.find_progress(file_id)
    return response

@app.get("/getall")
def get_all_data():
    response = db.fetch_all_data()
    return response

@app.delete("/delete_file")
def delete_file_by_name(file_id): 
    response = db.delete_file(file_id)
    return response

@app.delete("/reset_db")
def clear_database():
    response = db.clear_db()
    return response
