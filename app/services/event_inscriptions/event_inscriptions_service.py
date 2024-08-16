from app.database.models.event import EventStatus
from app.database.models.inscription import InscriptionModel
from app.exceptions.inscriptions_exceptions import InscriptionAlreadyExists, EventNotStarted
from app.repository.inscriptions_repository import InscriptionsRepository
from app.schemas.inscriptions.inscription import InscriptionRequestSchema, InscriptionResponseSchema
from app.services.events.events_service import EventsService
from app.services.services import BaseService
from app.services.storage.event_inscription_storage_service import EventInscriptionStorageService


class EventInscriptionsService(BaseService):
    def __init__(
            self,
            events_service: EventsService,
            storage_service: EventInscriptionStorageService,
            inscriptions_repository: InscriptionsRepository,
            event_id: str,
            user_id: str
    ):
        self.events_service = events_service
        self.storage_service = storage_service
        self.inscriptions_repository = inscriptions_repository
        self.event_id = event_id
        self.user_id = user_id

    async def inscribe_user_to_event(self, inscription: InscriptionRequestSchema):
        event_status = await self.events_service.get_event_status(self.event_id)
        if event_status != EventStatus.STARTED:
            raise EventNotStarted(self.event_id, event_status)
        if await self.inscriptions_repository.inscription_exists(self.event_id, self.user_id):
            raise InscriptionAlreadyExists(self.user_id, self.event_id)
        inscription = await self.inscriptions_repository.inscribe(self.event_id, self.user_id, inscription)
        upload_url = await self.storage_service.get_affiliation_upload_url(self.event_id, self.user_id, inscription.id)
        response = EventInscriptionsService.map_to_schema(inscription)
        response.affiliation_upload_url = upload_url
        return response

    @staticmethod
    def map_to_schema(model: InscriptionModel) -> InscriptionResponseSchema:
        return InscriptionResponseSchema(
            id=model.id,
            user_id=model.user_id,
            event_id=model.event_id,
            status=model.status,
            roles=model.roles,
            affiliation=model.affiliation
        )


"""
    async def get_event_inscriptions(self):
        resp = await self.inscriptions_repository.get_event_inscriptions(self.event_id)
        print(resp)
        return resp
"""
