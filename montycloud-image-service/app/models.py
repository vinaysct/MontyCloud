from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ImageMetadata(BaseModel):
    image_id: str
    user_id: str
    #tags: List[str] = []
    content_type: str
    created_at: datetime
    s3_key: str


class UploadImageResponse(BaseModel):
    image_id: str
    message: str = "Image uploaded successfully"


class ImageListResponse(BaseModel):
    image_id: str
    user_id: str
    #tags: List[str]
    #created_at: datetime

class ViewImageResponse(BaseModel):
    image_id: str
    url: str
    
class DeleteImageResponse(BaseModel):
    message: str = "Image deleted successfully"


class ErrorResponse(BaseModel):
    detail: str
