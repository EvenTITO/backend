from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.event import EventModel
from app.database.models.organizer import InvitationStatus, OrganizerModel
from app.repository.crud_repository import Repository


class EventsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EventModel)

    async def get_status(self, event_id: str):
        conditions = await self._primary_key_conditions(event_id)
        event_status = await self._get_with_values(conditions, EventModel.status)
        return event_status

    async def get_review_skeleton(self, event_id):
        conditions = await self._primary_key_conditions(event_id)
        review_skeleton = await self._get_with_values(conditions, EventModel.review_skeleton)
        return review_skeleton

    async def event_with_title_exists(self, title):
        conditions = [EventModel.title == title]
        return await self._exists_with_conditions(conditions)

    async def create(self, id_creator, event_create):
        new_event = EventModel(
            **event_create.model_dump(mode='json'),
            id_creator=id_creator
        )
        OrganizerModel(
            event=new_event,
            id_organizer=new_event.id_creator,
            invitation_status=InvitationStatus.ACCEPTED,
        )
        return await self._create(new_event)
