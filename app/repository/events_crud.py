from app.database.models.inscription import InscriptionModel
from app.database.models.user import UserModel, UserRole
from ..schemas.events.configuration_general import ConfigurationGeneralEventSchema
from ..schemas.events.public_event_with_roles import PublicEventWithRolesSchema
from ..schemas.events.review_skeleton.review_skeleton import ReviewSkeletonSchema
from ..database.models.event import EventModel, EventStatus
from ..schemas.events.schemas import (
    EventRol,
)
from sqlalchemy.future import select
from app.database.models.organizer import OrganizerModel
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_events_for_user(db: AsyncSession, user_id: str):
    inscriptions_q = (select(EventModel)
                      .join(InscriptionModel,
                            InscriptionModel.id_event == EventModel.id)
                      .where(InscriptionModel.id_inscriptor == user_id))

    organizations_q = (select(EventModel)
                       .join(OrganizerModel,
                             OrganizerModel.id_event == EventModel.id)
                       .where(OrganizerModel.id_organizer == user_id))

    inscr = db.execute(inscriptions_q)
    org = db.execute(organizations_q)
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


async def get_event_by_id(db: AsyncSession, event_id: str):
    event = await db.get(EventModel, event_id)
    return event

async def get_all_events(
    db: AsyncSession,
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
    result = await db.execute(query)
    return result.scalars().all()


async def is_creator(
    db: AsyncSession, event_id: str, user_id: str
):
    query = select(EventModel).where(
        EventModel.id == event_id,
        EventModel.id_creator == user_id
    )
    result = await db.execute(query)
    return result.scalars().first() is not None
