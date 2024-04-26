from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    name: str
    surname: str
    photo: str 
    email: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1234",
                    "name": "Pepe",
                    "surname": "Argento",
                    "photo": "base64-photo",
                    "email": "email@email.com"
                }
            ]
        }
    }
