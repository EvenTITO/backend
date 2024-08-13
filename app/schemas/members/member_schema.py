from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from app.schemas.users.user import UserSchema


class MemberInvitationStatus(str, Enum):
    INVITED = "INVITED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class MemberRequestSchema(BaseModel):
    email: str


class MemberResponseSchema(BaseModel):
    event_id: str
    user_id: str
    invitation_date: datetime
    invitation_status: MemberInvitationStatus
    user: UserSchema
