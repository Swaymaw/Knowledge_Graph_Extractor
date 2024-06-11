from fastapi import HTTPException
from utils import TextProcessing, genTripletGeneration
from bson.objectid import ObjectId
from database import genDatabase

db = genDatabase()

class PreprocessSteps:
    def __init__(self) -> None:
        self.my_col = db.my_col
        self.text_preprocess = TextProcessing()

    def extract_text_from_file(self, file_id):
        doc = self.my_col.find_one({"_id": ObjectId(file_id)})
        try:
            text = self.text_preprocess.extract_text_from_pdf(doc["byte"])
            self.my_col.update_one({"_id": ObjectId(file_id)}, {"$set": {"content": text}})
            db.update_progress(0, file_id)
            db.status_update("In Progress", file_id)
            return {"Updated Extracted Text"}
        except: 
            db.status_update("Failed", file_id)
            raise HTTPException(300, "File Couldn't be extracted")
        
    def text_cleanup_of_file(self, file_id):
        doc =  self.my_col.find_one({"_id": ObjectId(file_id)})
        try: 
            text = self.text_preprocess.text_cleanup(doc["content"])
            db.my_col.update_one({"_id": ObjectId(file_id)}, {"$set": {"content": text}})
            db.update_progress(1, file_id)
            return {"Updated Cleaned Text"}
        except:
            db.status_update("Failed", file_id)
            raise HTTPException(300, "File Couldn't be Cleaned")

    def triple_saver(self, file_id):
        doc =  self.my_col.find_one({"_id": ObjectId(file_id)})
        triplet_gen = genTripletGeneration()
        try: 
            triplets = triplet_gen.chunked_triplet_extractor(doc["content"])
            self.my_col.update_one({"_id": ObjectId(file_id)}, {"$set": {"triplets": triplets}})
            db.update_progress(2, file_id)
            db.status_update("Completed", file_id)
            return {"Successfully generate": f"Triplets for {file_id}"}
        except:
            db.status_update("Failed", file_id)
            raise HTTPException(300, "Triplets Couldn't Be generated")
        