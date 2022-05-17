from sqlalchemy import Column, Float, String, PickleType, Integer

from services.database import Base

from uuid import uuid4
from dataclasses import dataclass


@dataclass
class Product(Base):
    __tablename__ = 'products'
    # Core information
    id: int = Column(Integer, nullable=False, unique=True, primary_key=True)
    uuid: str = Column(String(36), default=str(uuid4()))
    name: str = Column(String, nullable=False, unique=True)
    brand: str = Column(String, nullable=False)
    price: float = Column(Float, nullable=False)

    # Unique product information
    category: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)
    image: str = Column(String, nullable=True)
    image_path: str = Column(String, nullable=False)
    original_link: str = Column(String, nullable=False)

    # Tracking and analytics information
    nutri_score: str = Column(String, nullable=True)
    quantity: str = Column(String, nullable=True)
    allergens: list = Column(PickleType, default=[], nullable=True)
    ingredients: list = Column(PickleType, default=[], nullable=True)

    # Product nutrition information
    energy: float = Column(Float, nullable=True)
    fat: float = Column(Float, nullable=True)
    saturated_fat: float = Column(Float, nullable=True)
    unsaturated_fat: float = Column(Float, nullable=True)
    carbohydrates: float = Column(Float, nullable=True)
    sugars: float = Column(Float, nullable=True)
    fiber: float = Column(Float, nullable=True)
    proteins: float = Column(Float, nullable=True)
    salt: float = Column(Float, nullable=True)
    extra: list = Column(PickleType, default=[], nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"
