from typing import Optional
from fastapi import Form
from pydantic import BaseModel
from datetime import datetime

class ImageCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    country: str
    birth_date: str
    passport: str
    phone: str
    qr_image: str
    image_path: str
    id_badge: Optional[str] = None


class ImageOut(BaseModel):
    id: str
    image_path: str
    qr_code_url: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PDFRequest(BaseModel):
    id: Optional[str] = None

class PDFResponse(BaseModel):
    id: str

    class Config:
        from_attributes = True