from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: str = Field(example="asjdfvhjbvnlaksdj")
    name: str = Field(example="Lio")
    surname: str = Field(example="Messi")
    photo: str = Field(description="base64 codified photo.",
                       example='base64-photo')
    email: str = Field(example="email@email.com")

    class Config:
        orm_mode = True
