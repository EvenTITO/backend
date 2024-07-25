from sqlalchemy import Column, String, ForeignKey, Integer, ARRAY, JSON
from app.database.database import Base


class SubmissionModel(Base):
    __tablename__ = "submissions"

    id_event = Column(String, ForeignKey("works.id_event"), primary_key=True)
    id_work = Column(Integer, ForeignKey("works.id"), primary_key=True)
    id = Column(Integer, primary_key=True)

    abstract = Column(String)
    keywords = Column(ARRAY(String), default='{}')
    authors = Column(JSON)

    review_decision = Column(String, nullable=True)
    review_comments = Column(String, nullable=True)
