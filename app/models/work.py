from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    UniqueConstraint,
    Integer,
    Date,
    ARRAY,
    JSON
)
from sqlalchemy.orm import relationship
from app.database.database import Base


class WorkModel(Base):
    __tablename__ = "works"

    id_event = Column(String, ForeignKey("events.id"), primary_key=True)
    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    track = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    keywords = Column(ARRAY(String), nullable=False)
    authors = Column(JSON, nullable=False)

    deadline_date = Column(Date, nullable=False)

    id_author = Column(String, ForeignKey("users.id"), nullable=False)
    id_reviewer = Column(String, ForeignKey("users.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint('id_event', 'title', name='event_id_title_uc'),
    )

    author = relationship(
        "UserModel",
        foreign_keys=[id_author],
        back_populates="works_as_author"
    )
    reviewer = relationship(
        "UserModel",
        foreign_keys=[id_reviewer],
        back_populates="works_as_reviewer"
    )
    event = relationship("EventModel", back_populates="works")

    submissions = relationship("SubmissionModel", back_populates="work")
