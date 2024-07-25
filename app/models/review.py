from sqlalchemy import Column, String, ForeignKey, Integer, JSON
from app.database.database import Base


class ReviewModel(Base):
    __tablename__ = "reviews"

    id_event = Column(
        String,
        ForeignKey("submissions.id_event"),
        primary_key=True
    )
    id_work = Column(
        Integer,
        ForeignKey("submissions.id_work"),
        primary_key=True
    )
    id_submission = Column(
        Integer,
        ForeignKey("submissions.id"),
        primary_key=True
    )
    id_reviewer = Column(String, ForeignKey("users.id"), primary_key=True)

    review = Column(JSON)
