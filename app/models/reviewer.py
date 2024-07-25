from app.utils.models_utils import DateTemplate
from datetime import datetime
from app.utils.exceptions import DatesException
from sqlalchemy import Column, String, Date
from app.database.database import Base
from sqlalchemy.orm import validates


class ReviewerModel(DateTemplate, Base):
    __tablename__ = "reviewer"

    id_user = Column(String, primary_key=True)
    id_event = Column(String, primary_key=True)

    invitation_expiration_date = Column(Date)
    invitation_status = Column(String, nullable=False)
    tracks = Column(String)

    @validates("invitation_expiration_date")
    def validate_date(self, key, invitation_expiration_date):
        if invitation_expiration_date is None:
            return datetime.now()
        if datetime.now() > invitation_expiration_date:
            raise DatesException()
        else:
            return invitation_expiration_date
