from sqlalchemy import String, Integer, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Car(Base):
    __tablename__ = "cars"

    __table_args__ = (
        UniqueConstraint("url", name="uq_car_url"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String)
    price_usd: Mapped[int]
    odometer: Mapped[int]
    username: Mapped[str]
    phone_number: Mapped[str]
    image_url: Mapped[str]
    images_count: Mapped[int]
    car_number: Mapped[str]
    car_vin: Mapped[str]
    datetime_found: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )
