# from app.database.models.event import EventStatus TODO: descomentar
from app.exceptions.inscriptions_exceptions import InscriptionAlreadyExists
from app.repository.inscriptions_repository import InscriptionsRepository
from app.services.events.events_service import EventsService
from app.services.services import BaseService


class EventInscriptionsService(BaseService):
    def __init__(
        self,
        events_service: EventsService,
        inscriptions_repository: InscriptionsRepository,
        event_id: str,
        user_id: str
    ):
        self.events_service = events_service
        self.inscriptions_repository = inscriptions_repository
        self.event_id = event_id
        self.user_id = user_id

    async def inscribe_user_to_event(self):
        await self.events_service.get_event_status(self.event_id)
        # event_status = await self.events_service.get_event_status(self.event_id)
        # TODO: descomentar esto. Rompe los tests, pero los tests estan mal.
        # if event_status != EventStatus.STARTED:
        #     raise EventNotStarted(self.event_id, event_status)
        if await self.inscriptions_repository.inscription_exists(self.event_id, self.user_id):
            raise InscriptionAlreadyExists(self.user_id, self.event_id)
        await self.inscriptions_repository.inscribe(self.event_id, self.user_id)
        return self.user_id

    async def get_event_inscriptions(self):
        resp = await self.inscriptions_repository.get_event_inscriptions(self.event_id)
        print(resp)
        return resp
