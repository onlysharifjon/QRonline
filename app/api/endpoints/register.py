from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from pathlib import Path
import qrcode
from app.schemas.image import *
from app.repositories.image_repository import ImageRepository
from app.core.database import get_db
from  ...models.image import *
router = APIRouter()

UPLOAD_DIR = Path("media")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
import os

@router.post('/pdf_upload', response_model = PDFResponse)
async def add_pdf(
        file: UploadFile = File(...),
        id: Optional[str] = Form(None),
        db: Session = Depends(get_db)
):
    # Generate ID if not provided
    document_id = id

    # Save the uploaded file
    upload_dir = "uploads/pdfs"
    os.makedirs(upload_dir, exist_ok = True)

    file_path = os.path.join(upload_dir, f"{document_id}_{file.filename}")

    # Write the file to disk
    with open(file_path, "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)

    # Create database entry
    pdf_document = PDFDocument(
        id = document_id,
        filename = file.filename,
        file_path = file_path
    )

    # Add to database
    db.add(pdf_document)
    db.commit()
    db.refresh(pdf_document)

    # Return response with only ID
    return PDFResponse(
        id = pdf_document.id
    )
    
    
    

@router.post("/register/", response_model=ImageOut)
async def register_image(
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: str = Form(None),
    country: str = Form("..."),
    birth_date: str = Form(...),
    passport: str = Form(...),
    phone: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    uid = str(uuid4())
    ext = image.filename.split(".")[-1]
    file_name = f"{uid}.{ext}"
    file_path = UPLOAD_DIR / file_name

    with open(file_path, "wb") as f:
        f.write(await image.read())

    # QR yaratish
    qr_link = f"http://qr.abdugafforov.uz:8000/view/{uid}"  # This represents the unique ID link for the QR code
    qr_img = qrcode.make(qr_link)
    qr_img.save(UPLOAD_DIR / f"{uid}_qr.png")

    image_data = ImageCreate(
        first_name = first_name,
        last_name = last_name,
        middle_name = middle_name,
        country = country,
        birth_date = birth_date,
        passport = passport,
        phone = phone,
        qr_image = f"/media/{uid}_qr.png",
        image_path = str(file_path)
    )

    image_repo = ImageRepository(db)
    image = image_repo.create(image_data, str(file_path))

    return {
        "id": image.id,
        "image_path": f"/media/{file_name}",
        "qr_code_url": f"/media/{uid}_qr.png",
        "created_at": image.created_at
    }
