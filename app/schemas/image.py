from pydantic import BaseModel
from datetime import datetime

class ImageCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None

class ImageOut(BaseModel):
    id: str
    image_path: str
    qr_code_url: str
    created_at: datetime

    class Config:
        orm_mode = True
