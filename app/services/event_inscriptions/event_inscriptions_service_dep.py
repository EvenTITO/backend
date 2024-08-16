from typing import Annotated

from fastapi import Depends

from app.authorization.caller_id_dep import CallerIdDep
from app.repository.inscriptions_repository import InscriptionsRepository
from app.repository.repository import get_repository
from app.services.event_inscriptions.event_inscriptions_service import EventInscriptionsService
from app.services.events.events_service_dep import EventsServiceDep
from app.services.storage.event_inscription_storage_service_dep import EventInscriptionStorageServiceDep


class EventInscriptionsServiceChecker:
    async def __call__(
            self,
            event_id: str,
            caller_id: CallerIdDep,
            events_service: EventsServiceDep,
            storage_service: EventInscriptionStorageServiceDep,
            inscriptions_repository: InscriptionsRepository = Depends(get_repository(InscriptionsRepository)),
    ) -> EventInscriptionsService:
        return EventInscriptionsService(events_service, storage_service, inscriptions_repository, event_id, caller_id)


event_inscriptions_checker = EventInscriptionsServiceChecker()
EventInscriptionsServiceDep = Annotated[EventInscriptionsService, Depends(event_inscriptions_checker)]
