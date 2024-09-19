from pydantic import BaseModel, Field

# TODO: capaz se podría usar DateSchema!


class Talk(BaseModel):
    date: str | None = Field(examples=["2024-01-01 09:00:00"], default=None)
    location: str | None = Field(
        max_length=200,
        examples=["FIUBA, Av. Paseo Colon 850"],
        default=""
    )
