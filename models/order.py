from sqlalchemy import Column, Float, String, PickleType, Integer, Boolean, DateTime

from services.database import Base

from uuid import uuid4
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Order(Base):
    """
    Order class representing an order for an event.\n
    An order is a grocery list that a user owns.
    """
    # TODO: Add methods to make database changes easier.
    __tablename__ = 'orders'
    # Core information
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True, )
    uuid: str = Column(String(36), nullable=False, default=str(uuid4()))
    user: str = Column(String, nullable=False)
    products: list = Column(PickleType, nullable=False, default=[])
    total_price: float = Column(Float, nullable=False)
    notes: str = Column(String, nullable=True, default=None)
    employee_notes: str = Column(String, nullable=True, default=None) # TODO: Implement this!

    # Unique tracking information
    event: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    last_changed_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    expired: bool = Column(Boolean, nullable=False, default=False)
    completed: bool = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Order {self.uuid}>"

