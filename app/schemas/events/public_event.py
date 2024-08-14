from pydantic import Field, computed_field

from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.event_status import EventStatusSchema
from app.schemas.media.image import ImgSchema
from app.services.storage.events_storage_service import EventsStorageService


class PublicEventSchema(CreateEventSchema, EventStatusSchema):
    id: str = Field(examples=["..."])

    @computed_field
    def media(self) -> list[ImgSchema]:
        return EventsStorageService.get_media(self.id)
