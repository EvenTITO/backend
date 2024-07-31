from app.database.models.utils import DateTemplate
from datetime import datetime
from app.exceptions.dates_exception import DatesException
from sqlalchemy import Column, String, Date
from app.database.database import Base
from sqlalchemy.orm import validates, relationship


class ChairModel(DateTemplate, Base):
    __tablename__ = "chairs"

    id_chair = Column(String, primary_key=True)
    id_event = Column(String, primary_key=True)

    invitation_expiration_date = Column(Date)
    invitation_status = Column(String, nullable=False)
    tracks = Column(String)

    chair = relationship("UserModel", back_populates="chairs")
    event = relationship("EventModel", back_populates="chairs")

    @validates("invitation_expiration_date") # todo esto queremos validarlo asi ??
    def validate_date(self, key, invitation_expiration_date):
        if invitation_expiration_date is None:
            return datetime.now()
        if datetime.now() > invitation_expiration_date:
            raise DatesException()
        else:
            return invitation_expiration_date
