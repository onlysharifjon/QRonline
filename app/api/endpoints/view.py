from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os

router = APIRouter()

UPLOAD_DIR = Path("media")

@router.get("/view/{uuid}")
def view_image(uuid: str):
    for file in os.listdir(UPLOAD_DIR):
        if file.startswith(uuid) and not file.endswith("_qr.png"):
            return FileResponse(UPLOAD_DIR / file)
    raise HTTPException(status_code=404, detail="Image not found")
