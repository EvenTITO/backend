from sqlalchemy import Column, String, Date
from app.database.database import Base


class EventModel(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    creation_date = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(String)
    event_type = Column(String)
    status = Column(String)

    def __repr__(self):
        return f"Event({self.id})"
