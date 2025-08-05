import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models import Base  # або просто from .models, якщо ти в тій же папці
from dotenv import load_dotenv
import os

load_dotenv()

async def init_models():
    engine = create_async_engine(os.getenv("LINK_DB"))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_models())