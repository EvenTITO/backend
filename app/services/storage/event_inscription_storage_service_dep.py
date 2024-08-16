from typing import Annotated

from fastapi import Depends

from app.services.storage.event_inscription_storage_service import EventInscriptionStorageService


class EventInscriptionStorage:
    async def __call__(self) -> EventInscriptionStorageService:
        return EventInscriptionStorageService()


event_inscription_storage_service = EventInscriptionStorage()
EventInscriptionStorageServiceDep = Annotated[
    EventInscriptionStorageService, Depends(event_inscription_storage_service)]
