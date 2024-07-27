from app.schemas.events.schemas import DynamicGeneralEventSchema


from pydantic import Field


class ConfigurationGeneralEventSchema(DynamicGeneralEventSchema):
    notification_mails: list[str] = Field(default_factory=list)
