from typing import Annotated

from fastapi import Depends

from app.services.storage.events_storage_service import EventsStorageService


class EventStorage:
    async def __call__(self) -> EventsStorageService:
        return EventsStorageService()


event_storage_service = EventStorage()
EventStorageServiceDep = Annotated[EventsStorageService, Depends(event_storage_service)]
