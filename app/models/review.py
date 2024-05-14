from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from app.models.user import UserModel
from app.models.event import EventModel


class ReviewModel(Base):
    __tablename__ = "review"
    work_id = Column(String, primary_key=True, nullable=False)
    author = Column(String, ForeignKey(UserModel.id),
                    primary_key=True, nullable=False)
    id_event = Column(
        String, ForeignKey(EventModel.id), primary_key=True, nullable=False
    )
    title = Column(String)
    work_state = Column(String)  # Approved, Waiting for Review, ...

    def __repr__(self):
        return (
            f"AcademicWork(work_id: {self.work_id}"
            f" | event: {self.id_event})"
        )
