from sqlalchemy import Column, String, ForeignKey, Integer, Date
from app.database.database import Base
from app.models.academic_work import AcademicWork
from app.models.event import EventModel


class SubmissionModel(Base):
    __tablename__ = "event_reviewer"
    submission_number = Column(Integer, primary_key=True)
    work_id = Column(
        String, ForeignKey(AcademicWork.id), primary_key=True, nullable=False
    )
    id_event = Column(
        String, ForeignKey(EventModel.id), primary_key=True, nullable=False
    )
    file_url = Column(String)
    abstract = Column(String, nullable=False)
    key_words = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    comments = Column(String)

    def __repr__(self):
        return f"Submission(reviewer: {self.id_reviewer}" f" | event: {self.id_event})"
