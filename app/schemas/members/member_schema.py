from pydantic import BaseModel

from app.schemas.events.schemas import EventRole
from app.schemas.users.user import UserSchema


class RolesRequestSchema(BaseModel):
    roles: list[EventRole]


class MemberRequestSchema(BaseModel):
    email: str
    role: EventRole


class MemberResponseSchema(BaseModel):
    event_id: str
    user_id: str
    user: UserSchema


class MemberResponseWithRolesSchema(MemberResponseSchema):
    roles: list[str]
