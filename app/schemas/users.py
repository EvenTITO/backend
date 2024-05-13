from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    id: str  # TODO: add validation uuid or firebase id.
    name: str = Field(min_length=2)
    surname: str = Field(min_length=2)
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1234",
                    "name": "Pepe",
                    "surname": "Argento",
                    "email": "email@email.com",
                }
            ]
        }
    }
