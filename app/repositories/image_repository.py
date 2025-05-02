import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.image import Image
from app.schemas.image import ImageCreate

class ImageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, image_data: ImageCreate, image_path: str) -> Image:
        image_id = str(uuid.uuid4())
        badge_id = image_data.id_badge or image_id  # id_badge = image_id bilan bir xil bo‘ladi

        new_image = Image(
            id=image_id,
            first_name=image_data.first_name,
            last_name=image_data.last_name,
            middle_name=image_data.middle_name,
            country=image_data.country,
            birth_date=image_data.birth_date,
            passport=image_data.passport,
            phone=image_data.phone,
            id_badge=badge_id,
            image_path=image_path,
            qr_image=image_data.qr_image
        )

        self.db.add(new_image)
        await self.db.commit()
        await self.db.refresh(new_image)

        return new_image
