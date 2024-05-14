from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base
from .models_utils import ModelTemplate
from app.models.user import UserModel
from app.models.event import EventModel


class EventInscriptionModel(ModelTemplate, Base):
    __tablename__ = "event_inscription"
    id_inscripted_user = Column(
        String, ForeignKey(UserModel.id), primary_key=True, nullable=False
    )
    id_event = Column(
        String, ForeignKey(EventModel.id), primary_key=True, nullable=False
    )
    payment_state = Column(String, nullable=False)
    payment_receipt_url = Column(String)

    def __repr__(self):
        return (
            f"EventInscription(inscripted_user: {self.id_inscripted_user}"
            f" | event: {self.id_event})"
        )
