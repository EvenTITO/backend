from app.inscriptions.model import InscriptionModel
from app.users.model import UserModel, UserRole
from .model import EventModel, EventStatus, ReviewerModel
from .schemas import EventRol, ReviewerSchema
from .schemas import EventModelWithRol, EventSchema, ReviewSkeletonSchema
from sqlalchemy.future import select
from app.organizers.model import InvitationStatus, OrganizerModel
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
                response[event.id] = EventModelWithRol(
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


async def create_event(db: AsyncSession, event: EventSchema,
                       user: UserModel):
    if user.role == UserRole.EVENT_CREATOR:
        status = EventStatus.CREATED
    else:
        status = EventStatus.WAITING_APPROVAL

    db_event = EventModel(**event.model_dump(), id_creator=user.id,
                          status=status)
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


# TODO: revisar porque en caso de dup PK se obtiene un error
async def create_reviewer(db: AsyncSession, reviewer: ReviewerSchema,
                          event_id: str, user_id: str):
    new_reviewer = ReviewerModel(**reviewer.model_dump(),
                                 id_user=user_id, id_event=event_id)
    db.add(new_reviewer)

    await db.commit()
    await db.refresh(new_reviewer)

    return new_reviewer


async def get_reviewer(db: AsyncSession, event_id: str, user_id: str):
    query = select(ReviewerModel).where(
        ReviewerModel.id_event == event_id,
        ReviewerModel.id_user == user_id
    )

    result = await db.execute(query)
    return result.scalars().first()


async def get_all_reviewer(db: AsyncSession, event_id: str):
    query = select(ReviewerModel).where(
        ReviewerModel.id_event == event_id
    )
    result = await db.execute(query)

    return result.scalars().all()
