from pydantic import Field

from app.schemas.events.schemas import DynamicGeneralEventSchema


class ConfigurationGeneralEventSchema(DynamicGeneralEventSchema):
    notification_mails: list[str] = Field(default_factory=list)
