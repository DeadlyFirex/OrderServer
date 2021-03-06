from sqlalchemy import Column, Float, String, Integer, Boolean, DateTime

from services.database import Base

from uuid import uuid4
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class Event(Base):
    """
    Event is an object orders are places upon.\n
    Every event ends at some point, indicating when employees order.
    """
    # TODO: Decide if this will be manual/automatic.
    # TODO: Add methods to make database changes easier.
    __tablename__ = 'events'
    # Core information
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String(36), nullable=False, default=str(uuid4()))

    # Unique tracking information
    active: bool = Column(Boolean, nullable=False, default=True)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    until: datetime = Column(DateTime, nullable=False, default=datetime.utcnow() + timedelta(days=7))
    deadline: datetime = Column(DateTime, nullable=False, default=datetime.utcnow() + timedelta(days=4))

    # Event unique settings
    max_order_price: float = Column(Float, nullable=False, default=20.0)

    def __repr__(self):
        return f"<Event {self.uuid}>"
