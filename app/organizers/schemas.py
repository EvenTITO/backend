from datetime import datetime
from pydantic import BaseModel
from app.events.schemas import EventSchema
from app.users.schemas import UserSchema


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
