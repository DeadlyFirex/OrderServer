from sqlalchemy import Column, Float, String, PickleType, Integer, Text

from services.database import Base

from uuid import uuid4
from dataclasses import dataclass


@dataclass
class Product(Base):
    """
    Product model representing a product.\n
    This product is what orders can be placed upon.\n
    """
    # TODO: Add methods to make database changes easier.
    __tablename__ = 'products'
    # Core information
    id: int = Column(Integer, nullable=False, unique=True, primary_key=True)
    uuid: str = Column(String(36), nullable=False, default=str(uuid4()))
    name: str = Column(String(50), nullable=False, unique=True)
    brand: str = Column(String(30), nullable=False)
    price: float = Column(Float, nullable=False)

    # Unique product information
    category: str = Column(String(30), nullable=False)
    description: str = Column(Text, nullable=False)
    image: str = Column(Text, nullable=False)
    image_path: str = Column(String(200), nullable=False)
    original_link: str = Column(String(200), nullable=False)

    # Tracking and analytics information
    nutri_score: str = Column(String(5), nullable=True)
    quantity: str = Column(String(10), nullable=True)
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
