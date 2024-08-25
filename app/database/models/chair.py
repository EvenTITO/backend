from sqlalchemy import Column, String, ARRAY

from app.database.models.base import Base
from app.database.models.member import MemberModel


class ChairModel(MemberModel, Base):
    __tablename__ = "chairs"
    tracks = Column(ARRAY(String))
