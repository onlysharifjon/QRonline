import uuid

from sqlalchemy.orm import Session
from app.models.image import Image
from app.schemas.image import ImageCreate


class ImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, image_data: ImageCreate, image_path: str) -> Image:
        # UUID generatsiya qilish
        image_id = str(uuid.uuid4())

        # Barcha kerakli maydonlarni to'ldirish
        new_image = Image(
            id = image_id,  # ID aniq berish
            first_name = image_data.first_name,
            last_name = image_data.last_name,
            middle_name = image_data.middle_name,
            country = image_data.country,  # Bu maydon etishmayapti
            birth_date = image_data.birth_date,  # Bu maydon etishmayapti
            passport = image_data.passport,  # Bu maydon etishmayapti
            phone = image_data.phone,  # Bu maydon etishmayapti
            id_badge = getattr(image_data, 'id_badge', ''),  # Agar mavjud bo'lmasa, bo'sh string
            image_path = image_path,
            qr_image = image_data.qr_image  # Bu maydon etishmayapti
        )

        self.db.add(new_image)
        self.db.commit()
        self.db.refresh(new_image)

        return new_image
