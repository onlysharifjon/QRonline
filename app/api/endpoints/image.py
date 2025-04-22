from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
from pathlib import Path
import qrcode

router = APIRouter()

UPLOAD_DIR = Path("media")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    uid = str(uuid4())
    filename = f"{uid}.{file_ext}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # QR code yaratish
    qr_link = f"http://localhost:8000/view/{uid}"
    qr_img = qrcode.make(qr_link)
    qr_path = UPLOAD_DIR / f"{uid}_qr.png"
    qr_img.save(qr_path)

    return {
        "uuid": uid,
        "image_url": f"/media/{filename}",
        "qr_code_url": f"/media/{uid}_qr.png",
        "scan_link": qr_link
    }
