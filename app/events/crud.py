from app.inscriptions.model import InscriptionModel
from .model import EventModel, EventStatus, EventRol
from .schemas import EventSchema, ReviewSkeletonSchema
from sqlalchemy.future import select
from sqlalchemy import union, literal
from app.organizers.model import OrganizerModel
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_events_for_user(db: AsyncSession, user_id: str):
    q = (select(literal(EventRol.SUSCRIBER).label('rol'),
                EventModel)
         .join(InscriptionModel, InscriptionModel.id_event == EventModel.id)
         .where(InscriptionModel.id_inscriptor == user_id))

    p = (select(literal(EventRol.ORGANIZER).label('rol'),
                EventModel)
         .join(OrganizerModel, OrganizerModel.id_event == EventModel.id)
         .where(OrganizerModel.id_organizer == user_id))
    union_events = union(p, q)
    events = await db.execute(union_events)
    events = events.mappings().all()

    return events


async def get_event_by_id(db: AsyncSession, event_id: str):
    return await db.get(EventModel, event_id)


async def get_event_by_title(db: AsyncSession, event_title: str):
    query = select(EventModel).where(EventModel.title == event_title)
    result = await db.execute(query)
    return result.scalars().first()


# async def get_event_by_user_id(db: AsyncSession, user_id: str):
#     query = select(EventModel).where(EventModel.title == event_title)
#     result = await db.execute(query)
#     return result.scalars().first()


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


async def create_event(db: AsyncSession, event: EventSchema, id_creator: str):
    db_event = EventModel(**event.model_dump(), id_creator=id_creator)
    db.add(db_event)
    await db.flush()

    db_organizer = OrganizerModel(
        id_organizer=id_creator,
        id_event=db_event.id
    )
    db.add(db_organizer)

    await db.commit()
    await db.refresh(db_event)
    return db_event


async def update_event(
    db: AsyncSession,
    current_event: EventModel,
    event_modification: EventSchema
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


async def update_review_skeleton(
    db: AsyncSession,
    event: EventModel,
    review_skeleton: ReviewSkeletonSchema
):
    event.review_skeleton = review_skeleton.review_skeleton
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


# async def delete_event(db: Session, event_id: str):
#     event = get_event_by_id(db, event_id)
#     db.delete(event)
#     db.commit()

#     return event
