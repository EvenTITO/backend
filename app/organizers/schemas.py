from datetime import datetime
from app.models.organizer import InvitationStatus
from pydantic import BaseModel, Field
from app.schemas.schemas import EventSchema
from app.schemas.users.user import UserSchema


class OrganizerRequestSchema(BaseModel):
    email_organizer: str


class OrganizerReplySchema(BaseModel):
    id_event: str
    id_organizer: str
    invitation_date: datetime


class OrganizerInEventResponseSchema(OrganizerReplySchema):
    organizer: UserSchema


class OrganizationsForUserSchema(OrganizerReplySchema):
    event: EventSchema


class ModifyInvitationStatusSchema(BaseModel):
    invitation_status: InvitationStatus = Field(
        examples=[InvitationStatus.INVITED])
