from pydantic import BaseModel

from app.schemas.members.member_schema import MemberResponseSchema


class ChairRequestSchema(BaseModel):
    tracks: list[str]


class ChairResponseSchema(MemberResponseSchema):
    tracks: list[str]
