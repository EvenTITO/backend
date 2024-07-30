from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.event import EventModel, EventStatus
from app.database.models.inscription import InscriptionModel
from app.database.models.organizer import InvitationStatus, OrganizerModel
from app.repository.crud_repository import Repository
from app.schemas.events.public_event_with_roles import PublicEventWithRolesSchema
from app.schemas.events.schemas import EventRol


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

    async def get_all_events_for_user(self, user_id: str, offset: int, limit: int) -> list[PublicEventWithRolesSchema]:
        # TODO: refactor query and whole method.
        inscriptions_q = (select(EventModel)
                        .join(InscriptionModel,
                                InscriptionModel.id_event == EventModel.id)
                        .where(InscriptionModel.id_inscriptor == user_id))

        organizations_q = (select(EventModel)
                        .join(OrganizerModel,
                                OrganizerModel.id_event == EventModel.id)
                        .where(OrganizerModel.id_organizer == user_id))

        inscr = self.session.execute(inscriptions_q)
        org = self.session.execute(organizations_q)
        inscr_result = await inscr
        org_result = await org
        inscriptions = inscr_result.scalars().all()
        organizations = org_result.scalars().all()

        def add_events(role, events, response):
            for event in events:
                print(event)
                if event.id in response:
                    response[event.id].roles.append(role)
                else:
                    response[event.id] = PublicEventWithRolesSchema(
                        id=event.id,
                        title=event.title,
                        dates=event.dates,
                        description=event.description,
                        event_type=event.event_type,
                        location=event.location,
                        tracks=event.tracks,
                        status=event.status,
                        roles=[role]
                    )
            return response
        response = {}
        response = add_events(EventRol.INSCRIPTED, inscriptions, response)
        response = add_events(EventRol.ORGANIZER, organizations, response)
        return list(response.values())

    async def get_all_events(
        self,
        offset: int,
        limit: int,
        status: EventStatus | None,
        title_search: str | None
    ):
        query = select(EventModel).offset(offset).limit(limit)
        if status is not None:
            query = query.where(EventModel.status == status)
        if title_search is not None:
            query = query.filter(EventModel.title.ilike(f'%{title_search}%'))
        result = await self.session.execute(query)
        return result.scalars().all()
