import asyncio
from app.core.database import Base, engine
from app.models import *  # barcha modellaringni yuklaydi

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Run qilish uchun
if __name__ == "__main__":
    asyncio.run(init_models())
