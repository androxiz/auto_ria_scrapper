import asyncio
from app.database import engine, Base
from app.scheduler import start_scheduler
from app import models

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await init_models()
    start_scheduler()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())

    
