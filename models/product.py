from uuid import uuid4
from services.database import Base
from sqlalchemy import Column, Float, String, PickleType, Integer


class Product(Base):
    __tablename__ = 'products'
    # Core information
    id = Column(Integer, nullable=False, unique=True)
    uuid = Column(String(36), primary_key=True, default=str(uuid4()))
    name = Column(String, nullable=False, unique=True)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Unique product information
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = NotImplemented

    # Tracking and analytics information
    nutri_score = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    allergens = Column(PickleType, default=[], nullable=True)
    ingredients = Column(PickleType, default=[], nullable=True)

    # Product nutrition information
    energy = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    saturated_fat = Column(Float, nullable=True)
    unsaturated_fat = Column(Float, nullable=True)
    carbohydrates = Column(Float, nullable=True)
    sugars = Column(Float, nullable=True)
    fiber = Column(Float, nullable=True)
    proteins = Column(Float, nullable=True)
    salt = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"
