from dataclasses import dataclass
from datetime import datetime
from hashlib import md5
from uuid import uuid4

from sqlalchemy import DateTime, Column, String, Integer

from services.database import Base
from services.utilities import Utilities


@dataclass
class Data(Base):
    """
    Data class, for tracking changes within the other tables.\n
    Update this using ``perform_changes()``.
    """
    __tablename__ = 'data'
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String(36), nullable=False, unique=True, default=str(uuid4()))

    # Tracking
    events_hash: str = Column(String(100), nullable=True, default=md5(Utilities.generate_secret().encode("UTF-8")).hexdigest())
    products_hash: str = Column(String(100), nullable=True, default=md5(Utilities.generate_secret().encode("UTF-8")).hexdigest())
    orders_hash: str = Column(String(100), nullable=True, default=md5(Utilities.generate_secret().encode("UTF-8")).hexdigest())
    users_hash: str = Column(String(100), nullable=True, default=md5(Utilities.generate_secret().encode("UTF-8")).hexdigest())

    # Time-tracking
    events_last_changed: datetime = Column(DateTime, nullable=True, default=datetime.utcnow())
    products_last_changed: datetime = Column(DateTime, nullable=True, default=datetime.utcnow())
    orders_last_changed: datetime = Column(DateTime, nullable=True, default=datetime.utcnow())
    users_last_changed: datetime = Column(DateTime, nullable=True, default=datetime.utcnow())

    def perform_changes(self, model):
        """
        Performs changes to the hash and last_changed values of the Data row model.\n
        Indicates changes to the given table. Automatically commits.\n
        |
        Valid values are ``events``, ``products``, ``orders`` and ``users``.\n
        :param model: String indicating table
        :return: Nothing
        """
        random_hash = md5(Utilities.generate_secret().encode("UTF-8")).hexdigest()
        time = datetime.utcnow()

        from services.database import db_session

        if model == "events":
            self.events_hash = random_hash
            self.events_last_changed = time
        elif model == "products":
            self.products_hash = random_hash
            self.products_last_changed = time
        elif model == "orders":
            self.orders_hash = random_hash
            self.orders_last_changed = time
        elif model == "users":
            self.users_hash = random_hash
            self.users_last_changed = time
        else:
            raise ValueError()
        db_session.commit()
        return

    def parsed(self):
        result = \
            {
                "id": 1,
                "uuid": self.uuid,

                "events_hash": self.events_hash,
                "events_last_changed": self.events_last_changed.isoformat(),

                "orders_hash": self.orders_hash,
                "orders_last_changed": self.orders_last_changed.isoformat(),

                "products_hash": self.products_hash,
                "products_last_changed": self.products_last_changed.isoformat(),

                "users_hash": self.users_hash,
                "users_last_changed": self.users_last_changed.isoformat(),
            },
        return result
