from sqlalchemy import Boolean, DateTime, Column, Integer, String, PickleType

from services.utilities import Utilities
from services.database import Base

from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime


@dataclass
class User(Base):
    # TODO: Add phone number/address if deemed necessary
    __tablename__ = 'users'
    # User-specific information
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String, nullable=False, unique=True, default=str(uuid4()))
    username: str = Column(String, nullable=False, unique=True)
    name: str = Column(String, nullable=False, unique=True)
    email: str = Column(String, nullable=False, unique=True)
    phone_number: str = Column(String, nullable=False, unique=True)
    address: str = Column(String, nullable=False, unique=True)
    postal_code: str = Column(String, nullable=False, unique=True)
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
    last_action: str = Column(String, nullable=True, default=None)
    last_login_at: datetime = Column(DateTime, nullable=True, default=None)
    last_login_ip: str = Column(String, nullable=True, default=None)
    login_count: int = Column(Integer, nullable=True, default=0)

    def get_fullname(self):
        return f"{self.initial}. {self.name}"

    def __repr__(self):
        return f"<User {self.get_fullname()}>"
