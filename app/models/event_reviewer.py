from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from app.models.user import UserModel
from app.models.event import EventModel


class EventReviewerModel(Base):
    __tablename__ = "event_reviewer"
    id_reviewer = Column(String,
                         ForeignKey(UserModel.id),
                         primary_key=True,
                         nullable=False)
    id_event = Column(String,
                      ForeignKey(EventModel.id),
                      primary_key=True,
                      nullable=False)

    def __repr__(self):
        return f"EventReviewer(reviewer: {self.id_reviewer}"\
               f" | event: {self.id_event})"
