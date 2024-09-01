from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.services.storage.event_storage_service import EventsStorageService


class EventStorage:
    async def __call__(self, event_id: UUID) -> EventsStorageService:
        return EventsStorageService(event_id)


event_storage_service = EventStorage()
EventStorageServiceDep = Annotated[EventsStorageService, Depends(event_storage_service)]
