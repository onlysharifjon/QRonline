from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    country = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    passport = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    id_badge = Column(String, default=lambda: str(uuid.uuid4()), nullable=False)
    image_path = Column(String, nullable=False)
    qr_image = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PDFDocument(Base):
    __tablename__ = "pdf_documents"

    id = Column(String, primary_key = True)
    filename = Column(String, nullable = False)
    file_path = Column(String, nullable = False)