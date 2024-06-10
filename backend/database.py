import pymongo 
from fastapi import HTTPException, File, UploadFile
from schema import MongoDataBase
from bson.objectid import ObjectId
import uuid
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from functools import lru_cache
from config import Config

@lru_cache(maxsize=1)
def genDatabase(): 
    return DatabaseControl()
class DatabaseControl: 
    def __init__(self) -> None:
        # setting up mongo connection
        self.myclient = pymongo.MongoClient(Config["mongo_port"]) 
        self.mydb = self.myclient[Config["mongo_db"]]
        self.my_col = self.mydb[Config["mongo_col"]]

    def update_progress(self, i, file_id): 
        try: 
            prog = self.my_col.find_one({"_id": ObjectId(file_id)})["kg_build_progress"]
            prog[i] = 1
            self.my_col.update_one({"_id": ObjectId(file_id)}, {"$set": {"kg_build_progress": prog}})
        except: 
            raise HTTPException(500, "Progress Update Failed")
    
    def jobid_update(self, file_id, jobid):
        self.my_col.update_one({"_id": ObjectId(file_id)}, {"$set": {"job_id": jobid}})
    
    def status_update(self, stat, file_id):
        self.my_col.update_one({"_id": ObjectId(file_id)}, {"$set": {"status": stat}})

    def save_file_content(self, file: UploadFile = File(...)):
        if not file.filename.endswith(".pdf"):
            raise HTTPException(500, "Bad Request / Only PDF Files accepted")
        # use of uuid is not necessary here
        data = MongoDataBase(_id=uuid.uuid4(), name=file.filename, created_on=str(datetime.now()), byte=str(file.file.read()))
        try: 
            x = self.my_col.insert_one(jsonable_encoder(data))
            self.status_update("Uploaded", x.inserted_id)
            return {"Successfully": f"Saved {x.inserted_id}"}
        except: 
            return {"Document Saving": "Failed"}
        
    def find_file(self, file_id): 
        document = self.my_col.find_one({"_id": ObjectId(file_id)})
        document["_id"] = str(document["_id"])      
        if document: 
            return {"File Content": document["content"]}
        raise HTTPException(404, "File not Found")
    
    def fetch_all_data(self):
        items = list(self.my_col.find({}))
        for item in items:
            item["_id"] = str(item["_id"])
        return {"data": items} 
    
    def find_progress(self, file_id): 
        document = self.my_col.find_one({"_id": ObjectId(file_id)})
        document["_id"] = str(document["_id"])      
        if document: 
            return {"File Content": document["kg_build_progress"], "File Status": document["status"]}
        raise HTTPException(404, "File not Found")
    
    def find_triplets(self, file_id):
        document =   self.my_col.find_one({"_id": ObjectId(file_id)})
        if not document: 
            raise HTTPException(404, "File not Found")
        triplet_list = document["triplets"]
        if len(triplet_list) == 0:
            raise HTTPException(405, "Make sure you first generate the triplets before getting them.")
        return {"Triplets List": triplet_list}

    def delete_file(self, file_id): 
        try: 
            self.my_col.delete_one({"_id": ObjectId(file_id)})
            return {"Successfully": f"Deleted {file_id}"}
        except:
            raise HTTPException(404, f"{file_id} Not Found")

    def clear_db(self):
        x = self.my_col.delete_many({})
        return {"Deleted Count": x.deleted_count}
    
