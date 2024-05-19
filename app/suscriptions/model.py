from enum import Enum
from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.utils.models_utils import ModelTemplate


class SuscriptionStatus(str, Enum):
    PAYMENT_INCOMPLETED = "PAYMENT_INCOMPLETED"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"


class SuscriptionModel(ModelTemplate, Base):
    __tablename__ = "suscriptions"

    id_suscriptor = Column(String, ForeignKey("users.id"))
    id_event = Column(String, ForeignKey("events.id"))
    status = Column(
        String, default=SuscriptionStatus.PAYMENT_INCOMPLETED.value)

    suscriptor = relationship("UserModel", back_populates="suscriptions")
    event = relationship("EventModel", back_populates="suscriptions")

    def to_dict(self):
        return {
            "id_suscriptor": self.id_suscriptor,
            "id_event": self.id_event,
            "status": self.status,
        }
