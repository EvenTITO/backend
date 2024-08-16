from app.database.models.event import EventStatus
from app.database.models.inscription import InscriptionModel, InscriptionStatus
from app.exceptions.inscriptions_exceptions import EventNotStarted, InscriptionAlreadyPaid, \
    InscriptionNotFound
from app.repository.inscriptions_repository import InscriptionsRepository
from app.schemas.inscriptions.inscription import InscriptionRequestSchema, InscriptionResponseSchema, \
    InscriptionPayResponseSchema
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
        saved_inscription = await self.inscriptions_repository.inscribe(self.event_id, self.user_id, inscription)
        response = EventInscriptionsService.map_to_schema(saved_inscription)
        if saved_inscription.affiliation is not None:
            upload_url = await self.storage_service.get_affiliation_upload_url(
                self.event_id,
                self.user_id,
                saved_inscription.id
            )
            response.affiliation_upload_url = upload_url
        return response

    async def get_event_inscriptions(self, offset: int, limit: int) -> list[InscriptionResponseSchema]:
        inscriptions = await self.inscriptions_repository.get_event_inscriptions(self.event_id, offset, limit)
        return list(map(EventInscriptionsService.map_to_schema, inscriptions))

    async def get_my_event_inscriptions(self, offset: int, limit: int) -> list[InscriptionResponseSchema]:
        inscriptions = await self.inscriptions_repository.get_event_user_inscriptions(
            self.event_id,
            self.user_id,
            offset,
            limit
        )
        return list(map(EventInscriptionsService.map_to_schema, inscriptions))

    async def get_my_inscription(self, inscription_id: str) -> InscriptionResponseSchema:
        inscription = await self.inscriptions_repository.get_user_inscription_by_id(self.user_id, inscription_id)
        return EventInscriptionsService.map_to_schema(inscription)

    async def pay(self, inscription_id: str) -> InscriptionPayResponseSchema:
        my_inscription = await self.get_my_inscription(inscription_id)
        if my_inscription is None:
            raise InscriptionNotFound(self.event_id, inscription_id)
        if my_inscription.status != InscriptionStatus.PENDING_PAYMENT:
            raise InscriptionAlreadyPaid(inscription_id, self.user_id, self.event_id)
        await self.inscriptions_repository.pay(inscription_id)
        upload_url = await self.storage_service.get_payment_upload_url(self.event_id, self.user_id, inscription_id)
        return InscriptionPayResponseSchema(id=inscription_id, upload_url=upload_url)

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
