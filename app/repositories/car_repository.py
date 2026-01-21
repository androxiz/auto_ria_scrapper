from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import AsyncSessionLocal
from app.models.car import Car

class CarRepository:

    @staticmethod
    async def exists(url: str) -> bool:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Car.id).where(Car.url == url)
            )
            return result.scalar() is not None

    @staticmethod
    async def create(data: dict):
        async with AsyncSessionLocal() as session:
            car = Car(**data)
            session.add(car)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
