from sqlalchemy import Column, String, Date
from app.database.database import Base


class EventModel(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    creation_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)
    type_of_event = Column(String)
    state_of_event = Column(String)

    def __repr__(self):
        return f"Event({self.id})"
