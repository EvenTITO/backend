from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from app.models.user import UserModel
from app.models.event import EventModel


class EventOrganizerModel(Base):
    __tablename__ = "event_organizer"
    id_organizer = Column(String,
                          ForeignKey(UserModel.id),
                          primary_key=True,
                          nullable=False)
    id_event = Column(String,
                      ForeignKey(EventModel.id_event),
                      primary_key=True,
                      nullable=False)

    def __repr__(self):
        return f"EventOrganizer(organizer: {self.id_organizer}"\
               f" | event: {self.id_event})"
