from pydantic import BaseModel, EmailStr, Field
from .model import UserPermission


class UserSchema(BaseModel):
    name: str = Field(min_length=2)
    surname: str = Field(min_length=2)
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Pepe",
                    "surname": "Argento",
                    "email": "email@email.com",
                }
            ]
        }
    }


class UserSchemaWithId(UserSchema):
    id: str


class RoleSchema(BaseModel):
    role: UserPermission


class CompleteUser(UserSchemaWithId, RoleSchema):
    id: str
