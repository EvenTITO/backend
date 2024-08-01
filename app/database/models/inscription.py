from enum import Enum
from sqlalchemy import Column, String, ForeignKey
from app.database.models.base import Base
from sqlalchemy.orm import relationship
from app.database.models.utils import DateTemplate


class InscriptionStatus(str, Enum):
    PAYMENT_INCOMPLETED = "PAYMENT_INCOMPLETED"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"


class InscriptionModel(DateTemplate, Base):
    __tablename__ = "inscriptions"

    inscriptor_id = Column(String, ForeignKey("users.id"), primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), primary_key=True)
    status = Column(
        String, default=InscriptionStatus.PAYMENT_INCOMPLETED.value
    )

    inscriptor = relationship("UserModel", back_populates="inscriptions")
    event = relationship("EventModel", back_populates="inscriptions")

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "status": self.status,
        }
