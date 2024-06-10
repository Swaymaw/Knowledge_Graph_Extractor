from pydantic import BaseModel 


Config = {
            "origin": "http://localhost:3000",
            "mongo_port": "mongodb://localhost:27017/",
            "mongo_db": "file_data",
            "mongo_col": "uploaded_files",
            "redis_port": "redis://localhost:6379",
        }

