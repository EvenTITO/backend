from enum import Enum

from sqlalchemy import Column, String

from app.database.models.base import Base
from app.database.models.utils import DateTemplate, UIDType


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    EVENT_CREATOR = "EVENT_CREATOR"
    DEFAULT = "DEFAULT"


class UserModel(DateTemplate, Base):
    __tablename__ = "users"
    id = Column(UIDType, primary_key=True)

    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    role = Column(String, default=UserRole.DEFAULT.value)
    identification_number = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
