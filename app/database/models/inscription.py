from enum import Enum

from sqlalchemy import Column, String, ForeignKey, Integer, ARRAY, Index
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.utils import DateTemplate


class InscriptionStatus(str, Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_MADE = "PAYMENT_MADE"
    CONFIRMED_PAYMENT = "CONFIRMED_PAYMENT"


class InscriptionRole(str, Enum):
    SPEAKER = "SPEAKER"
    ATTENDEE = "ATTENDEE"


class InscriptionModel(DateTemplate, Base):
    __tablename__ = "inscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), )
    event_id = Column(String, ForeignKey("events.id"))
    status = Column(String, default=InscriptionStatus.PENDING_PAYMENT.value, nullable=False)
    roles = Column(ARRAY(String), default=[InscriptionRole.ATTENDEE.value], nullable=False)
    affiliation = Column(String, default=None, nullable=True)

    user = relationship("UserModel", back_populates="inscriptions")
    event = relationship("EventModel", back_populates="inscriptions")
    __table_args__ = (
        Index('ix_inscription_user_id', 'user_id'),
        Index('ix_inscription_event_id', 'event_id'),
    )
