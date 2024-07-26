from fastapi import APIRouter
from app.storage.events_storage import EventsStaticFiles, get_upload_url
from app.storage.schemas import UploadURLSchema
from app.organizers.dependencies import EventOrganizerDep


events_media_router = APIRouter(
    prefix="/{event_id}/upload_url",
    tags=["Events: Multimedia"]
)


@events_media_router.get("/main_image")
async def get_main_image_upload_url(
    _: EventOrganizerDep,
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.MAIN_IMAGE)


@events_media_router.get("/banner_image")
async def get_banner_image_upload_url(
    _: EventOrganizerDep,
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.BANNER_IMAGE)


@events_media_router.get("/brochure")
async def get_brochure_upload_url(
    _: EventOrganizerDep,
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.BROCHURE)
