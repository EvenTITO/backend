from pydantic import BaseModel, Field, EmailStr
from app.schemas.users.user_role import UserRoleSchema


class UserSchema(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Pepe"])
    lastname: str = Field(min_length=2, max_length=100, examples=["Argento"])
    email: EmailStr = Field(examples=["pepe.argento@email.com"])


class UserReply(UserSchema, UserRoleSchema):
    id: str