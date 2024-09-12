from uuid import UUID

from app.repository.payments_repository import PaymentsRepository
from app.schemas.payments.payment import PaymentRequestSchema, PaymentsResponseSchema
from app.schemas.users.utils import UID
from app.services.services import BaseService
from app.services.storage.event_inscription_storage_service import EventInscriptionStorageService


class EventPaymentsService(BaseService):
    def __init__(
            self,
            storage_service: EventInscriptionStorageService,
            payments_repository: PaymentsRepository,
            event_id: UUID,
            user_id: UID
    ):
        self.storage_service = storage_service
        self.payments_repository = payments_repository
        self.event_id = event_id
        self.user_id = user_id

    async def pay_inscription(self, inscription_id: UUID, payment_request: PaymentRequestSchema) -> UUID:
        return await self.payments_repository.do_new_payment(self.event_id, inscription_id, payment_request)

    async def get_event_payments(self, offset: int, limit: int) -> list[PaymentsResponseSchema]:
        return await self.payments_repository.get_all_payments_for_event(self.event_id, offset, limit)
