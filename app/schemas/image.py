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
    created_at: datetime

    class Config:
        orm_mode = True
