from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from app.schemas.users.user import UserSchema


class MemberInvitationStatus(str, Enum):
    INVITED = "INVITED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class MemberRequestSchema(BaseModel):
    email: str


class MemberResponseSchema(BaseModel):
    id_event: str
    id_user: str
    invitation_date: datetime
    user: UserSchema


class ModifyInvitationStatusSchema(BaseModel):
    invitation_status: MemberInvitationStatus = Field(
        examples=[MemberInvitationStatus.INVITED])

