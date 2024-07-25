from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    UniqueConstraint,
    Integer,
    Date
)
from sqlalchemy.orm import relationship
from app.database.database import Base


class WorkModel(Base):
    __tablename__ = "works"

    id_event = Column(String, ForeignKey("events.id"), primary_key=True)
    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    track = Column(String, nullable=False)
    stage = Column(String, nullable=False)

    deadline_date = Column(Date)

    id_author = Column(String, ForeignKey("users.id"), nullable=False)
    id_reviewer = Column(String, ForeignKey("users.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint('id_event', 'title', name='event_id_title_uc'),
    )

    author = relationship("UserModel", back_populates="works")
    event = relationship("EventModel", back_populates="works")
    reviewer = relationship("UserModel", back_populates="works")
