from pydantic import BaseModel
from datetime import datetime


class InscriptorRequestSchema(BaseModel):
    id_inscriptor: str


class InscriptionSchema(InscriptorRequestSchema):
    id_event: str


class InscriptionReplySchema(InscriptionSchema):
    status: str
    creation_date: datetime
