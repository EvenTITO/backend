from app.schemas.events.public_event import PublicEventSchema


from pydantic import ConfigDict, Field


class PublicEventWithRolesSchema(PublicEventSchema):
    model_config = ConfigDict(from_attributes=True)
    roles: list[str] = Field(
        examples=[["ORGANIZER"]],
        default=[]
    )
