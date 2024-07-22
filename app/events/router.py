from typing import List
from app.storage.events_storage import EventsStaticFiles, get_upload_url
from app.storage.schemas import UploadURLSchema
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
    DatesCompleteSchema,
    EventSchema,
    EventSchemaWithEventId,
    FullEventSchema,
    PricingRateSchema,
    EventStatusSchema,
    EventModelWithRol,
    EventRol,
    ReviewSkeletonSchema, ReviewerSchema, ReviewerSchemaComplete,
    GeneralEventSchema
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


@events_router.get("/{event_id}/public", response_model=EventModelWithRol)
async def read_event_general(event_id: str, db: SessionDep,
                             X_User_Id: str = Header(...)):
    event = await get_event(db, event_id)
    event.roles = []
    event = EventModelWithRol.model_validate(event)
    if not X_User_Id:
        return event
    if await is_organizer(db, event_id, X_User_Id):
        event.roles.append(EventRol.ORGANIZER)
    return event


@events_router.get("/{event_id}/configuration")
async def get_event_configuration(
    _: EventOrganizerDep,
    event_id: str,
    db: SessionDep
) -> FullEventSchema:
    event = await get_event(db, event_id)
    return event


@events_router.put("/{event_id}/general", status_code=204, response_model=None)
async def update_general_event(
    _: EventOrganizerDep,
    event_id: str,
    event_modification: GeneralEventSchema,
    db: SessionDep
):
    current_event = await get_event(db, event_id)
    await validations.validate_update(db, current_event, event_modification)
    await crud.update_event(db, current_event, event_modification)


@events_router.put("/{event_id}/dates", status_code=204, response_model=None)
async def update_dates_event(
    _: EventOrganizerDep,
    event_id: str,
    dates_modification: DatesCompleteSchema,
    db: SessionDep
):
    current_event = await get_event(db, event_id)
    await crud.update_dates(db, current_event, dates_modification)


@events_router.put("/{event_id}/pricing", status_code=204, response_model=None)
async def update_pricing_event(
    _: EventOrganizerDep,
    event_id: str,
    pricing_modification: PricingRateSchema,
    db: SessionDep
):
    current_event = await get_event(db, event_id)
    await crud.update_pricing(db, current_event, pricing_modification)


@events_router.patch(
    "/{event_id}/status",
    status_code=204,
    response_model=None
)
async def change_event_status(
        caller: CallerUserDep,
        event_id: str,
        status_modification: EventStatusSchema,
        db: SessionDep
):
    event = await get_event(db, event_id)
    await validations.validate_status_change(
        db, caller, event, status_modification
    )
    await crud.update_status(db, event, status_modification.status)


@events_router.get(
    "/{event_id}/review-skeleton",
    status_code=200
)
async def get_review_skeleton(
        _: EventOrganizerDep,
        caller: CallerUserDep,
        event_id: str,
        db: SessionDep
) -> ReviewSkeletonSchema:
    return await crud.get_review_sckeletor(db, event_id, caller.id)


@events_router.get(
    "/{event_id}/pricing",
    status_code=200
)
async def get_pricing(
        caller: CallerUserDep,
        event_id: str,
        db: SessionDep
) -> PricingRateSchema:
    return await crud.get_pricing(db, event_id, caller.id)


@events_router.get(
    "/{event_id}/dates",
    status_code=200
)
async def get_dates(
        caller: CallerUserDep,
        event_id: str,
        db: SessionDep
) -> DatesCompleteSchema:
    return await crud.get_dates(db, event_id, caller.id)


@events_router.put(
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


@events_router.get("/{event_id}/upload_url/main_image")
async def get_main_image_upload_url(
    _: EventOrganizerDep,
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.MAIN_IMAGE)


@events_router.get("/{event_id}/upload_url/banner_image")
async def get_banner_image_upload_url(
    _: EventOrganizerDep,
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.BANNER_IMAGE)


@events_router.get("/{event_id}/upload_url/brochure")
async def get_brochure_upload_url(
    _: EventOrganizerDep,
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.BROCHURE)


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
