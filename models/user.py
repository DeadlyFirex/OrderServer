from sqlalchemy import Boolean, DateTime, Column, Integer, String, PickleType

from services.utilities import Utilities
from services.database import Base

from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime
from inspect import currentframe


@dataclass
class User(Base):
    """
    User model representing a user.\n
    This is either an admin, allowing to make changes to the microservice.\n
    But usually someone that is able to see products, events and orders to place new orders.
    """
    # TODO: Add methods to make database changes easier.
    __tablename__ = 'users'
    # User-specific information
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String, nullable=False, unique=True, default=str(uuid4()))
    username: str = Column(String, nullable=False, unique=True)
    name: str = Column(String, nullable=False, unique=True)
    email: str = Column(String, nullable=False, unique=True)
    phone_number: str = Column(String, nullable=False, unique=True)
    address: str = Column(String, nullable=False)
    postal_code: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    country: str = Column(String, nullable=True, default="NL")

    # Clearance/security/authentication
    flags: list = Column(PickleType, nullable=False, default=[])
    admin: bool = Column(Boolean, nullable=False, default=False)
    password: str = Column(String, nullable=False)
    secret: str = Column(String, nullable=True, unique=True, default=Utilities.generate_secret())
    token: str = Column(String, nullable=True, unique=True, default=None)
    tags: list = Column(PickleType, nullable=False, default=[])

    # Tracking
    active: bool = Column(Boolean, nullable=True, default=None)
    last_action_at: datetime = Column(DateTime, nullable=True, default=None)
    last_action_ip: str = Column(String, nullable=True, default=None)
    last_action: str = Column(String, nullable=True, default=None)
    last_login_at: datetime = Column(DateTime, nullable=True, default=None)
    last_login_ip: str = Column(String, nullable=True, default=None)
    login_count: int = Column(Integer, nullable=True, default=0)

    def get_fullname(self):
        return f"{self.name[0]}. {self.name.split(' ')[1]}"

    def perform_tracking(self, source: str = None, address: str = "UNKNOWN", active: bool = True, login: bool = False):
        from services.database import db_session
        now = datetime.utcnow()

        if source is None:
            source = str(currentframe().f_back.f_code.co_name)

        if login:
            self.active = active
            self.login_count += 1
            self.last_login_at = now
            self.last_login_ip = address
        else:
            self.active = active
            self.last_action = source
            self.last_action_at = now
            self.last_action_ip = address

        db_session.commit()

    def __repr__(self):
        return f"<User {self.get_fullname()}>"
