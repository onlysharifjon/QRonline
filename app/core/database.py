from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# Asinxron engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base model
Base = declarative_base()

# DB dependency
async def get_db():
    async with async_session_maker() as session:
        yield session
