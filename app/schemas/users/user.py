from pydantic import BaseModel, Field, EmailStr

from app.schemas.users.user_role import UserRoleSchema


class UserModifySchema(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Pepe"])
    lastname: str = Field(min_length=2, max_length=100, examples=["Argento"])
    identification_number: int | None = Field(min_length=2, max_length=100, examples=[12345678], default=None)
    phone: int | None = Field(min_length=8, max_length=13, examples=[5491165501111], default=None)
    address: str | None = Field(min_length=2, max_length=100, examples=["Paseo Colon 850"], default=None)
    city: str | None = Field(min_length=2, max_length=100, examples=["Ciudad Autónoma de Buenos Aires"], default=None)
    country: str | None = Field(min_length=2, max_length=100, examples=["Argentina"], default=None)


class UserSchema(UserModifySchema):
    email: EmailStr = Field(examples=["pepe.argento@email.com"])


class UserReply(UserSchema, UserRoleSchema):
    id: str
