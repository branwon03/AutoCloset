from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from s3_service import generate_presigned_upload_url
from database import engine
import models

# This command tells SQLAlchemy to create the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UploadUrlRequest(BaseModel):
    file_type: str

@app.get("/")
def read_root():
    return {"message": "API connected successfully!"}

@app.post("/api/media/presigned-url")
def get_upload_url(request: UploadUrlRequest):
    try:
        data = generate_presigned_upload_url(request.file_type)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))