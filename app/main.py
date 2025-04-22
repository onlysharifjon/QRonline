from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import image, view,register
app = FastAPI()

app.include_router(image.router)
app.include_router(view.router)

# media papkani statik fayllar uchun ochamiz
app.mount("/media", StaticFiles(directory="media"), name="media")


app.include_router(register.router)
