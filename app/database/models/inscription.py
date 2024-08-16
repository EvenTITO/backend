from enum import Enum

from sqlalchemy import Column, String, ForeignKey, Integer, ARRAY, Index
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.utils import DateTemplate


class InscriptionStatus(str, Enum):
    PAYMENT_INCOMPLETE = "PAYMENT_INCOMPLETE"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"


class InscriptionRole(str, Enum):
    SPEAKER = "SPEAKER"
    ATTENDEE = "ATTENDEE"


class InscriptionModel(DateTemplate, Base):
    __tablename__ = "inscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), )
    event_id = Column(String, ForeignKey("events.id"))
    status = Column(String, default=InscriptionStatus.PAYMENT_INCOMPLETE.value, nullable=False)
    roles = Column(ARRAY(String), default=[InscriptionRole.ATTENDEE.value], nullable=False)
    affiliation = Column(String, default=None, nullable=True)

    user = relationship("UserModel", back_populates="inscriptions")
    event = relationship("EventModel", back_populates="inscriptions")
    __table_args__ = (
        Index('ix_event_id_user_id', 'event_id', 'user_id'),
    )
