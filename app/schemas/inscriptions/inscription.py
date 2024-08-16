from typing import Self

from pydantic import BaseModel, model_validator, ConfigDict

from app.database.models.inscription import InscriptionRole, InscriptionStatus


class InscriptionRequestSchema(BaseModel):
    roles: list[InscriptionRole]
    affiliation: str | None

    @model_validator(mode='after')
    def check_mandatory_roles(self) -> Self:
        if self.roles is None or len(self.roles) == 0:
            raise ValueError("There must be at least one role in the inscription.")
        return self


class InscriptionResponseSchema(BaseModel):
    id: str
    user_id = str
    event_id = str
    roles: list[InscriptionRole]
    status = InscriptionStatus
    affiliation: str | None
    affiliation_upload_url: str | None


class InscriptionPayResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    upload_url: str
