from pydantic import (
    BaseModel,
    Field,
    model_validator,
)
from datetime import datetime
from typing_extensions import Self
from app.database.models.organizer import InvitationStatus

class ChairRequestSchema(BaseModel):
    email_organizer: str

class ReviewerSchema(BaseModel):
    invitation_expiration_date: datetime | None = \
        Field(examples=[datetime(2024, 12, 9)], default=None)
    invitation_status: str = Field(examples=[InvitationStatus.INVITED])
    tracks: str | None = Field(max_length=1000,
                               examples=["track1, track2, track3"],
                               default=None)

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.invitation_expiration_date <= datetime.now():
            raise ValueError('Invalid invitation expiration date.')
        return self


class ReviewerSchemaComplete(ReviewerSchema):
    id_user: str = Field(examples=["..."])
