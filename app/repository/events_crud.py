from app.models.inscription import InscriptionModel
from app.models.user import UserModel, UserRole
from ..schemas.events.configuration_general import ConfigurationGeneralEventSchema
from ..schemas.events.public_event_with_roles import PublicEventWithRolesSchema
from ..schemas.events.review_skeleton.review_skeleton import ReviewSkeletonSchema
from ..models.event import EventModel, EventStatus
from ..schemas.events.schemas import (
    DatesCompleteSchema,
    EventRol,
    PricingSchema,
)
from ..schemas.events.create_event import (
    CreateEventSchema
)
from sqlalchemy.future import select
from app.models.organizer import InvitationStatus, OrganizerModel
from sqlalchemy.ext.asyncio import AsyncSession


async def get_dates(db: AsyncSession, event_id: str, user_id: str):
    query = select(EventModel.dates).where(
        EventModel.id == event_id,
        EventModel.id_creator == user_id
    )

    result = await db.execute(query)
    return result.scalars().first()


async def get_pricing(db: AsyncSession, event_id: str, user_id: str):
    query = select(EventModel.pricing).where(
        EventModel.id == event_id,
        EventModel.id_creator == user_id
    )

    result = await db.execute(query)
    return result.scalars().first()


async def get_review_sckeletor(db: AsyncSession, event_id: str, user_id: str):
    query = select(EventModel.review_skeleton).where(
        EventModel.id == event_id,
        EventModel.id_creator == user_id
    )

    result = await db.execute(query)
    return result.scalars().first()


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
                    start_date=event.start_date,
                    end_date=event.end_date,
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
    return await db.get(EventModel, event_id)


async def get_event_by_title(db: AsyncSession, event_title: str):
    query = select(EventModel).where(EventModel.title == event_title)
    result = await db.execute(query)
    return result.scalars().first()


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


async def create_event(db: AsyncSession, event: CreateEventSchema,
                       user: UserModel):
    if user.role == UserRole.EVENT_CREATOR:
        status = EventStatus.CREATED
    else:
        status = EventStatus.WAITING_APPROVAL

    db_event = EventModel(
        **event.model_dump(),
        id_creator=user.id,
        status=status,
        notification_mails=[]
    )
    db.add(db_event)
    await db.flush()

    db_organizer = OrganizerModel(
        id_organizer=user.id,
        id_event=db_event.id,
        invitation_status=InvitationStatus.ACCEPTED,
    )
    db.add(db_organizer)

    await db.commit()
    await db.refresh(db_event)
    return db_event


async def update_general_event(
        db: AsyncSession,
        current_event: EventModel,
        event_modification
):
    orig_title = current_event.title
    for attr, value in event_modification.model_dump().items():
        setattr(current_event, attr, value)
    current_event.title = orig_title
    await db.commit()
    await db.refresh(current_event)

    return current_event


async def update_event(
    db: AsyncSession,
    current_event: EventModel,
    event_modification: ConfigurationGeneralEventSchema
):
    for attr, value in event_modification.model_dump().items():
        setattr(current_event, attr, value)
    await db.commit()
    await db.refresh(current_event)

    return current_event


async def update_status(
    db: AsyncSession,
    event: EventModel,
    status_modification: EventStatus
):
    event.status = status_modification
    await db.commit()
    await db.refresh(event)
    return event


async def update_pricing(
    db: AsyncSession,
    event: EventModel,
    pricing: PricingSchema
):
    event.pricing = pricing.model_dump()
    await db.commit()
    await db.refresh(event)
    return event


async def update_dates(
    db: AsyncSession,
    event: EventModel,
    dates: DatesCompleteSchema
):
    event.start_date = dates.start_date
    event.end_date = dates.end_date
    event.dates = dates.model_dump(mode='json')
    await db.commit()
    await db.refresh(event)
    return event


async def update_review_skeleton(
    db: AsyncSession,
    event: EventModel,
    review_skeleton: ReviewSkeletonSchema
):
    event.review_skeleton = review_skeleton.model_dump()
    await db.commit()
    await db.refresh(event)
    return event


async def is_creator(
    db: AsyncSession, event_id: str, user_id: str
):
    query = select(EventModel).where(
        EventModel.id == event_id,
        EventModel.id_creator == user_id
    )
    result = await db.execute(query)
    return result.scalars().first() is not None
