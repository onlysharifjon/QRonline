from pathlib import Path
import qrcode
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from typing import Optional
import os
import aiofiles
from app.core.database import get_db
from app.models.image import PDFDocument
from app.repositories.image_repository import ImageRepository
from app.schemas.image import PDFResponse, ImageCreate, ImageOut

router = APIRouter()

UPLOAD_DIR = Path("media")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post('/pdf_upload', response_model=PDFResponse)
async def add_pdf(
    file: UploadFile = File(...),
    id: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    document_id = id or str(uuid4())

    upload_dir = "uploads/pdfs"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{document_id}_{file.filename}")

    async with aiofiles.open(file_path, "wb") as buffer:
        contents = await file.read()
        await buffer.write(contents)

    pdf_document = PDFDocument(
        id=document_id,
        filename=file.filename,
        file_path=file_path
    )

    db.add(pdf_document)

    try:
        await db.commit()
        await db.refresh(pdf_document)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Ushbu ID ({document_id}) bilan hujjat allaqachon mavjud."
        )

    return PDFResponse(id=pdf_document.id)


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
    db: AsyncSession = Depends(get_db)
):
    uid = str(uuid4())
    ext = image.filename.split(".")[-1]
    file_name = f"{uid}.{ext}"
    file_path = UPLOAD_DIR / file_name

    with open(file_path, "wb") as f:
        f.write(await image.read())

    qr_link = f"http://qr.abdugafforov.uz:8000/view/{uid}"
    qr_img = qrcode.make(qr_link)
    qr_img.save(UPLOAD_DIR / f"{uid}_qr.png")

    image_data = ImageCreate(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        country=country,
        birth_date=birth_date,
        passport=passport,
        phone=phone,
        qr_image=f"/media/{uid}_qr.png",
        image_path=str(file_path),
        id_badge=uid  # ID bilan bir xil bo‘ladi
    )

    image_repo = ImageRepository(db)
    image = await image_repo.create(image_data, str(file_path))  # ⚠️ await qilish shart

    return {
        "id": image.id,
        "image_path": f"/media/{file_name}",
        "qr_code_url": f"/media/{uid}_qr.png",
        "created_at": image.created_at
    }
