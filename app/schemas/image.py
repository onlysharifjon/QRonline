from typing import Optional

from fastapi import Form
from pydantic import BaseModel
from datetime import datetime

class ImageCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    country: str  # Bu maydon etishmayapti
    birth_date: str  # Bu maydon etishmayapti
    passport: str  # Bu maydon etishmayapti
    phone: str  # Bu maydon etishmayapti
    qr_image: str  # Bu maydon etishmayapti

class ImageOut(BaseModel):
    id: str
    image_path: str
    qr_code_url: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class PDFResponse(BaseModel):
    id: str

    class Config:
        orm_mode = True


# Pydantic model for request
class PDFRequest(BaseModel):
    id: Optional[str] = None