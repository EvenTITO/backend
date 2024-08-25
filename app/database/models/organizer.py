from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.member import MemberModel


class OrganizerModel(MemberModel, Base):
    __tablename__ = "organizers"
    event = relationship("EventModel", back_populates="organizers")
