from pydantic import BaseModel, Field


class AuthorInformation(BaseModel):
    full_name: str = Field(examples=['Juan Sanchez'])
    membership: str = Field(examples=['FIUBA'])
    mail: str = Field(examples=['juansanchez@mail.com'])
    notify_updates: bool = Field(description=(
        'If set to true, the author will receive emails '
        'with the work updates (reviews, deadline date notification)'
    ),
        default=False
    )