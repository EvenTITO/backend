from enum import Enum

from sqlalchemy import Column, String, ForeignKey, DateTime

from app.database.models.utils import DateTemplate


class InvitationStatus(str, Enum):
    INVITED = "INVITED"
    ACCEPTED = "ACCEPTED"


class MemberModel(DateTemplate):
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), primary_key=True)
    invitation_expiration_date = Column(DateTime, nullable=True)
    invitation_status = Column(String, default=InvitationStatus.INVITED.value)
