from pydantic import BaseModel, ConfigDict
from typing import List


class SuscriptionSchema(BaseModel):
    id_suscriptor: str
    id_event: str


class UserSuscription(BaseModel):
    id: str


class SuscriptionReplySchema(SuscriptionSchema):
    status: str


class GetSuscriptionReplySchema(BaseModel):
    suscriptions: List[dict]

    model_config = ConfigDict(from_attributes=True)
