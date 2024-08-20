from pydantic import BaseModel

from app.schemas.users.user import UserSchema


class MemberRequestSchema(BaseModel):
    email: str
    role: str


class MemberResponseSchema(BaseModel):
    event_id: str
    user_id: str
    user: UserSchema


class MemberResponseWithRolesSchema(MemberResponseSchema):
    roles: list[str]
