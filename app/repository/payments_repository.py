from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.payment import PaymentModel
from app.repository.crud_repository import Repository
from app.schemas.payments.payment import PaymentRequestSchema, PaymentsResponseSchema


class PaymentsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PaymentModel)

    async def get_all_payments_for_event(self, event_id: UUID, offset: int, limit: int) -> list[PaymentsResponseSchema]:
        conditions = [PaymentModel.event_id == event_id]
        return await self._get_payments(conditions, offset, limit)

    async def do_new_payment(self, event_id: UUID, inscription_id: UUID, payment_request: PaymentRequestSchema) -> UUID:
        new_payment = PaymentModel(
            **payment_request.model_dump(),
            event_id=event_id,
            inscription_id=inscription_id
        )
        return (await self._create(new_payment)).id

    async def _get_payments(
            self,
            conditions,
            offset: int,
            limit: int
    ) -> list[PaymentsResponseSchema]:
        res = await self._get_many_with_conditions(conditions, offset, limit)
        return [
            PaymentsResponseSchema(
                id=row.id,
                event_id=row.event_id,
                inscription_id=row.inscription_id,
                status=row.status,
                works=row.works,
                fare_name=row.fare_name
            ) for row in res
        ]
