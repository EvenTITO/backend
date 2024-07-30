from app.schemas.events.create_event import CreateEventSchema
from app.schemas.events.event_status import EventStatusSchema
from app.schemas.media.image import ImgSchema
from app.services.storage.events_storage import EventsStaticFiles, get_public_event_url


from pydantic import Field, computed_field


class PublicEventSchema(CreateEventSchema, EventStatusSchema):
    id: str = Field(examples=["..."])

    @computed_field
    def media(self) -> list[ImgSchema]:
        return [
            ImgSchema(
                name='main_image_url',
                url=get_public_event_url(self.id, EventsStaticFiles.MAIN_IMAGE)
            ),
            ImgSchema(
                name='brochure_url',
                url=get_public_event_url(self.id, EventsStaticFiles.BROCHURE)
            ),
            ImgSchema(
                name='banner_image_url',
                url=get_public_event_url(
                    self.id, EventsStaticFiles.BANNER_IMAGE),
            )
        ]
