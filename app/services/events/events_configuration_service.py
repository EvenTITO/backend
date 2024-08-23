from app.database.models.event import EventStatus
from app.exceptions.events_exceptions import CannotUpdateTracksAfterEventStarts
from app.repository.events_repository import EventsRepository
from app.schemas.events.configuration import EventConfigurationSchema
from app.schemas.events.configuration_general import ConfigurationGeneralEventSchema
from app.schemas.events.dates import DatesCompleteSchema
from app.schemas.events.pricing import PricingSchema
from app.schemas.events.review_skeleton.review_skeleton import ReviewSkeletonSchema
from app.schemas.events.schemas import DynamicTracksEventSchema
from app.services.services import BaseService


class EventsConfigurationService(BaseService):
    def __init__(self, events_repository: EventsRepository, event_id: str):
        self.events_repository = events_repository
        self.event_id = event_id

    async def get_configuration(self) -> EventConfigurationSchema:
        return await self.events_repository.get(self.event_id)

    async def update_pricing(self, pricing: PricingSchema) -> None:
        await self.events_repository.update(self.event_id, pricing)

    async def update_review_skeleton(self, review_skeleton: ReviewSkeletonSchema) -> None:
        await self.events_repository.update(self.event_id, review_skeleton)

    async def update_dates(self, dates: DatesCompleteSchema) -> None:
        await self.events_repository.update(self.event_id, dates)

    async def update_general(self, general: ConfigurationGeneralEventSchema) -> None:
        event = await self.events_repository.get(self.event_id)
        if event.status == EventStatus.STARTED and set(event.tracks) != set(general.tracks):
            raise CannotUpdateTracksAfterEventStarts(self.event_id)
        await self.events_repository.update(self.event_id, general)

    async def update_tracks(self, tracks_schema: DynamicTracksEventSchema) -> None:
        event = await self.events_repository.get(self.event_id)
        if event.status == EventStatus.STARTED and set(event.tracks) != set(tracks_schema.tracks):
            raise CannotUpdateTracksAfterEventStarts(self.event_id)
        await self.events_repository.update_tracks(self.event_id, tracks_schema.tracks)

    async def get_review_skeleton(self) -> ReviewSkeletonSchema:
        review_skeleton = await self.events_repository.get_review_skeleton(self.event_id)
        return ReviewSkeletonSchema(
            review_skeleton=review_skeleton
        )
