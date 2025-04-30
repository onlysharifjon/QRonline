from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import image, view,register

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.include_router(image.router)
app.include_router(view.router)

# media papkani statik fayllar uchun ochamiz
app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # yoki ["http://localhost:5173"] — xavfsizroq
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router)
