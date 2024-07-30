from pydantic import BaseModel
from datetime import datetime

from app.schemas.events.create_event import CreateEventSchema
from app.schemas.users.user import UserSchema


class InscriptionReplySchema(BaseModel):
    id_event: str
    id_inscriptor: str
    status: str
    creation_date: datetime


class InscriptionsInEventResponseSchema(InscriptionReplySchema):
    inscripted_user: UserSchema


class InscriptionsForUserSchema(InscriptionReplySchema):
    event: CreateEventSchema
