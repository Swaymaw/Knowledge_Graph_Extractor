from pydantic import BaseModel
from typing import List, Optional


class MongoDataBase(BaseModel): 
    _id: str 
    name: str 
    created_on: str
    job_id: Optional[str] = ""
    byte: str
    status: Optional[str] = "Pending"
    kg_build_progress: Optional[List] = [0]*3
    content: Optional[str] = ""
    triplets: Optional[List] = []