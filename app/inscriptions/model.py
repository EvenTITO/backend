from enum import Enum
from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.utils.models_utils import DateTemplate


class InscriptionStatus(str, Enum):
    PAYMENT_INCOMPLETED = "PAYMENT_INCOMPLETED"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"


class InscriptionModel(DateTemplate, Base):
    __tablename__ = "inscriptions"

    id_inscriptor = Column(String, ForeignKey("users.id"), primary_key=True)
    id_event = Column(String, ForeignKey("events.id"), primary_key=True)
    status = Column(
        String, default=InscriptionStatus.PAYMENT_INCOMPLETED.value
    )

    inscriptor = relationship("UserModel", back_populates="inscriptions")
    event = relationship("EventModel", back_populates="inscriptions")

    def to_dict(self):
        return {
            "id_event": self.id_event,
            "status": self.status,
        }
