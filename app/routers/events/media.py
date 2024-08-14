from fastapi import APIRouter, Depends

from app.authorization.organizer_or_admin_dep import verify_is_organizer
from app.schemas.storage.schemas import UploadURLSchema
from app.services.storage.event_storage_service_dep import EventStorageServiceDep
from app.services.storage.events_storage_service import EventsStaticFiles

events_media_router = APIRouter(
    prefix="/{event_id}/upload_url",
    tags=["Events: Multimedia"]
)


@events_media_router.get(path="/{media}", dependencies=[Depends(verify_is_organizer)])
async def get_upload_url(
        event_id: str,
        media: EventsStaticFiles,
        storage_service: EventStorageServiceDep
) -> UploadURLSchema:
    return await storage_service.get_upload_url(event_id, media)
