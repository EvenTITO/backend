from pydantic import BaseModel, Field


class AuthorInformation(BaseModel):
    full_name: str = Field(examples=['Juan Sanchez'])
    membership: str = Field(examples=['FIUBA'])
    mail: str = Field(examples=['juansanchez@mail.com'])
