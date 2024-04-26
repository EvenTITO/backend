from sqlalchemy import Column, String
from .database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    photo = Column(String)
    email = Column(String, unique=True)


    def __repr__(self):
        return f"User({self.id})"
    def __str__(self):
        return f"User({self.id})"
