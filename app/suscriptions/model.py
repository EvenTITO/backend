from enum import Enum
from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship


class SuscriptionStatus(str, Enum):
    PAYMENT_INCOMPLETED = "PAYMENT_INCOMPLETED"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"


class SuscriptionModel(Base):
    __tablename__ = "suscriptions"

    id_suscriptor = Column(String, ForeignKey("users.id"), primary_key=True)
    id_event = Column(String, ForeignKey("events.id"), primary_key=True)
    status = Column(
        String, default=SuscriptionStatus.PAYMENT_INCOMPLETED.value
    )

    suscriptor = relationship("UserModel", back_populates="suscriptions")
    event = relationship("EventModel", back_populates="suscriptions")

    def to_dict(self):
        return {
            "id_event": self.id_event,
            "status": self.status,
        }
