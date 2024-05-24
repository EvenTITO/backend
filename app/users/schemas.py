from pydantic import BaseModel, EmailStr, Field
from .model import UserRole


class UserSchema(BaseModel):
    name: str = Field(min_length=2, examples=["Pepe"])
    lastname: str = Field(min_length=2, examples=["Argento"])
    email: EmailStr = Field(examples=["pepe.argento@email.com"])


class RoleSchema(BaseModel):
    role: UserRole


class UserReply(UserSchema, RoleSchema):
    id: str
