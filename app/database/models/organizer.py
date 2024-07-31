from sqlalchemy.orm import relationship

from app.database.database import Base
from app.database.models.member import MemberModel


class OrganizerModel(MemberModel, Base):
    __tablename__ = "organizers"
    organizer = relationship("UserModel", back_populates="organizers")
    event = relationship("EventModel", back_populates="organizers")
