from typing import List
from fastapi import APIRouter, Header, Query
from app.database.dependencies import SessionDep
from app.events.dependencies import GetEventsQuerysDep
from app.events.model import EventStatus
from app.organizers.crud import is_organizer
from app.users.dependencies import CallerUserDep
from app.organizers.dependencies import EventOrganizerDep
from app.events import crud, validations
import app.notifications.events as notifications
from .utils import get_event
from .schemas import (
    CompleteEventSchema,
    EventSchema,
    EventSchemaWithEventId,
    ModifyEventStatusSchema,
    EventModelWithRol,
    ReviewSkeletonSchema,
    EventRol, ReviewerSchema, ReviewerSchemaComplete
)

events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.get("/my-events", response_model=List[EventModelWithRol])
async def read_my_events(
        db: SessionDep,
        caller_user: CallerUserDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    return await crud.get_all_events_for_user(db, caller_user.id)


@events_router.get("/", response_model=List[EventSchemaWithEventId])
async def read_all_events(
        db: SessionDep,
        status_query: GetEventsQuerysDep,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
        search: str | None = None
):
    print('El valor de la query es')
    print(status_query)
    return await crud.get_all_events(
        db=db,
        offset=offset,
        limit=limit,
        status=status_query,
        title_search=search
    )


@events_router.post("", status_code=201, response_model=str)
async def create_event(
        event: EventSchema,
        caller_user: CallerUserDep,
        db: SessionDep
):
    await validations.validate_event_not_exists(db, event)
    event_created = await crud.create_event(
        db=db,
        event=event,
        user=caller_user
    )
    if event_created.status == EventStatus.WAITING_APPROVAL:
        await notifications.request_approve_event(
            db, caller_user, event_created
        )
    return event_created.id


@events_router.get("/{event_id}", response_model=CompleteEventSchema)
async def read_event(event_id: str, db: SessionDep,
                     X_User_Id: str = Header(...)):
    event = await get_event(db, event_id)
    event = CompleteEventSchema.model_validate(event)
    if not X_User_Id:
        return event
    if await is_organizer(db, event_id, X_User_Id):
        event.roles.append(EventRol.ORGANIZER)
    return event


@events_router.put("/{event_id}", status_code=204, response_model=None)
async def update_event(
        _: EventOrganizerDep,
        event_id: str,
        event_modification: EventSchema,
        db: SessionDep
):
    current_event = await get_event(db, event_id)
    await validations.validate_update(db, current_event, event_modification)
    await crud.update_event(db, current_event, event_modification)


@events_router.patch(
    "/{event_id}/status",
    status_code=204,
    response_model=None
)
async def change_event_status(
        caller: CallerUserDep,
        event_id: str,
        status_modification: ModifyEventStatusSchema,
        db: SessionDep
):
    event = await get_event(db, event_id)
    await validations.validate_status_change(
        db, caller, event, status_modification
    )
    await crud.update_status(db, event, status_modification.status)


@events_router.patch(
    "/{event_id}/review-skeleton",
    status_code=204,
    response_model=None
)
async def change_review_skeleton(
        _: EventOrganizerDep,
        event_id: str,
        review_skeleton: ReviewSkeletonSchema,
        db: SessionDep
):
    event = await get_event(db, event_id)
    await crud.update_review_skeleton(db, event, review_skeleton)


@events_router.post("/{event_id}/reviewer/{user_id}", status_code=201)
async def create_reviewer(
        event_id: str,
        user_id: str,
        reviewer: ReviewerSchema,
        _: EventOrganizerDep,
        db: SessionDep
):
    await validations.validate_unique_reviewer(db, event_id, user_id)

    reviewer_created = await crud.create_reviewer(
        db=db,
        reviewer=reviewer,
        event_id=event_id,
        user_id=user_id
    )
    return reviewer_created


@events_router.get(
    "/{event_id}/reviewer",
    response_model=List[ReviewerSchemaComplete])
async def get_reviewer(
        event_id: str,
        db: SessionDep,
        _: EventOrganizerDep
):
    return await crud.get_all_reviewer(db, event_id)
