from sqlalchemy import DateTime, Column, String, Integer

from services.database import Base
from services.utilities import Utilities

from dataclasses import dataclass
from uuid import uuid4
from hashlib import md5
from datetime import datetime


@dataclass
class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String, nullable=False, unique=True, default=str(uuid4()))

    # Tracking
    events_hash: str = Column(String, nullable=True, default=md5(Utilities.generate_secret().encode("UTF-8")).hexdigest())
    products_hash: str = Column(String, nullable=True, default=md5(Utilities.generate_secret().encode("UTF-8")).hexdigest())
    orders_hash: str = Column(String, nullable=True, default=md5(Utilities.generate_secret().encode("UTF-8")).hexdigest())
    users_hash: str = Column(String, nullable=True, default=md5(Utilities.generate_secret().encode("UTF-8")).hexdigest())

    # Time-tracking
    events_last_changed: datetime = Column(DateTime, nullable=True, default=datetime.utcnow())
    products_last_changed: datetime = Column(DateTime, nullable=True, default=datetime.utcnow())
    orders_last_changed: datetime = Column(DateTime, nullable=True, default=datetime.utcnow())
    users_last_changed: datetime = Column(DateTime, nullable=True, default=datetime.utcnow())

    def generate_hash(self, model):
        result = md5(Utilities.generate_secret().encode("UTF-8")).hexdigest()
        if model == "events":
            self.events_hash = result
        elif model == "products":
            self.products_hash = result
        elif model == "orders":
            self.orders_hash = result
        elif model == "users":
            self.users_hash = result
        else:
            raise ValueError()

    def generate_timestamp(self, model):
        result = datetime.utcnow()
        if model == "events":
            self.events_last_changed = result
        elif model == "products":
            self.products_last_changed = result
        elif model == "orders":
            self.orders_last_changed = result
        elif model == "users":
            self.users_last_changed = result
        else:
            raise ValueError()
