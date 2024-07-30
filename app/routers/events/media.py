from fastapi import APIRouter, Depends
from app.services.storage.events_storage import EventsStaticFiles, get_upload_url
from app.schemas.storage.schemas import UploadURLSchema
from app.authorization.organizer_or_admin_dep import verify_is_organizer


events_media_router = APIRouter(
    prefix="/{event_id}/upload_url",
    tags=["Events: Multimedia"]
)


@events_media_router.get("/main_image", dependencies=[Depends(verify_is_organizer)])
async def get_main_image_upload_url(
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.MAIN_IMAGE)


@events_media_router.get("/banner_image", dependencies=[Depends(verify_is_organizer)])
async def get_banner_image_upload_url(
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.BANNER_IMAGE)


@events_media_router.get("/brochure", dependencies=[Depends(verify_is_organizer)])
async def get_brochure_upload_url(
    event_id: str,
) -> UploadURLSchema:
    return get_upload_url(event_id, EventsStaticFiles.BROCHURE)
