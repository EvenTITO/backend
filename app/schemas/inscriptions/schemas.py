from pydantic import BaseModel
from datetime import datetime

from app.schemas.events.create_event import CreateEventSchema
from app.schemas.users.user import UserSchema


class InscriptionReplySchema(BaseModel):
    event_id: str
    inscriptor_id: str
    status: str
    creation_date: datetime


class InscriptionsInEventResponseSchema(InscriptionReplySchema):
    inscripted_user: UserSchema


class InscriptionsForUserSchema(InscriptionReplySchema):
    event: CreateEventSchema
