from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from pathlib import Path
import qrcode
from app.schemas.image import ImageCreate, ImageOut
from app.repositories.image_repository import ImageRepository
from app.core.database import get_db

router = APIRouter()

UPLOAD_DIR = Path("media")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/register/", response_model=ImageOut)
async def register_image(
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    uid = str(uuid4())
    ext = file.filename.split(".")[-1]
    file_name = f"{uid}.{ext}"
    file_path = UPLOAD_DIR / file_name

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # QR yaratish
    qr_link = f"http://localhost:8000/view/{uid}"
    qr_img = qrcode.make(qr_link)
    qr_img.save(UPLOAD_DIR / f"{uid}_qr.png")

    image_data = ImageCreate(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name
    )

    image_repo = ImageRepository(db)
    image = image_repo.create(image_data, str(file_path))

    return {
        "id": image.id,
        "image_path": f"/media/{file_name}",
        "qr_code_url": f"/media/{uid}_qr.png",
        "created_at": image.created_at
    }
