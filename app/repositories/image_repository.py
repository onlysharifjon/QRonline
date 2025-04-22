from sqlalchemy.orm import Session
from app.models.image import Image
from app.schemas.image import ImageCreate

class ImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, image_data: ImageCreate, image_path: str) -> Image:
        new_image = Image(
            first_name=image_data.first_name,
            last_name=image_data.last_name,
            middle_name=image_data.middle_name,
            image_path=image_path
        )
        self.db.add(new_image)
        self.db.commit()
        self.db.refresh(new_image)
        return new_image
