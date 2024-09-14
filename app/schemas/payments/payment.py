from uuid import UUID

from pydantic import ConfigDict, Field, BaseModel

from app.database.models.payment import PaymentStatus
from app.schemas.storage.schemas import UploadURLSchema


class PaymentIdSchema(BaseModel):
    id: UUID


class PaymentUploadSchema(PaymentIdSchema):
    model_config = ConfigDict(from_attributes=True)
    upload_url: UploadURLSchema | None = Field(default=None)


class PaymentRequestSchema(BaseModel):
    fare_name: str = Field(examples=["tarifa de speaker"])
    works: list[str] | None


class PaymentsResponseSchema(PaymentIdSchema):
    event_id: UUID
    inscription_id: UUID
    status: PaymentStatus
    fare_name: str = Field(examples=["tarifa de speaker"])
    works: list[str] | None
