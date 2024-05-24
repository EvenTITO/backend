from pydantic import BaseModel
from datetime import datetime


class SuscriptorRequestSchema(BaseModel):
    id_suscriptor: str


class SuscriptionSchema(SuscriptorRequestSchema):
    id_event: str


class SuscriptionReplySchema(SuscriptionSchema):
    status: str
    creation_date: datetime
