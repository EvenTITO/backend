from enum import Enum

from sqlalchemy import Column, String, ForeignKey, ARRAY, Index

from app.database.models.base import Base
from app.database.models.utils import ModelTemplate


class InscriptionStatus(str, Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_MADE = "PAYMENT_MADE"
    CONFIRMED_PAYMENT = "CONFIRMED_PAYMENT"


class InscriptionRole(str, Enum):
    SPEAKER = "SPEAKER"
    ATTENDEE = "ATTENDEE"


class InscriptionModel(ModelTemplate, Base):
    __tablename__ = "inscriptions"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    status = Column(String, default=InscriptionStatus.PENDING_PAYMENT.value, nullable=False)
    roles = Column(ARRAY(String), default=[InscriptionRole.ATTENDEE.value], nullable=False)
    affiliation = Column(String, default=None, nullable=True)

    __table_args__ = (
        Index('ix_inscription_user_id', 'user_id'),
        Index('ix_inscription_event_id', 'event_id'),
    )
