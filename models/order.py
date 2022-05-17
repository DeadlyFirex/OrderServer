from sqlalchemy import Column, Float, String, PickleType, Integer, Boolean, DateTime

from services.database import Base

from uuid import uuid4
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Order(Base):
    __tablename__ = 'orders'
    # Core information
    id: int = Column(Integer, nullable=False, unique=True, primary_key=True)
    uuid: str = Column(String(36), primary_key=True, default=str(uuid4()))
    user: str = Column(String, nullable=False)
    products: list = Column(PickleType, nullable=False, default=[])
    total_price: float = Column(Float, nullable=False)
    notes: str = Column(String, nullable=True, default=None)

    # Unique tracking information
    event: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    last_changed_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    open: bool = Column(Boolean, nullable=False, default=True)
    completed: bool = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Order {self.name}>"

