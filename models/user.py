from uuid import uuid4
from services.utilities import Utilities
from services.database import Base
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Column, Integer, String, PickleType


class User(Base):
    __tablename__ = 'users'
    # User-specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String, nullable=False, unique=True, default=str(uuid4()))
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    country = Column(String, nullable=True, default="NL")

    # Clearance/security/authentication
    flags = Column(PickleType, nullable=False, default=[])
    admin = Column(Boolean, nullable=False, default=False)
    password = Column(String, nullable=False)
    secret = Column(String, nullable=True, unique=True, default=Utilities.generate_secret())
    token = Column(String, nullable=True, unique=True, default=None)
    tags = Column(PickleType, nullable=False, default=[])

    # Tracking
    active = Column(Boolean, nullable=True, default=None)
    last_action_at = Column(DateTime, nullable=True, default=None)
    last_action = Column(String, nullable=True, default=None)
    last_login_at = Column(DateTime, nullable=True, default=None)
    last_login_ip = Column(String, nullable=True, default=None)
    login_count = Column(Integer, nullable=True, default=0)

    def get_fullname(self):
        return f"{self.initial}. {self.name}"

    def __repr__(self):
        return f"<User {self.get_fullname()}>"
