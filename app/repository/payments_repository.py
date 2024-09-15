from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.payment import PaymentModel
from app.repository.crud_repository import Repository
from app.schemas.payments.payment import PaymentRequestSchema, PaymentsResponseSchema, PaymentStatusSchema


class PaymentsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PaymentModel)

    async def get_all_payments_for_event(self, event_id: UUID, offset: int, limit: int) -> list[PaymentsResponseSchema]:
        conditions = [PaymentModel.event_id == event_id]
        return await self._get_payments(conditions, offset, limit)

    async def get_payment(self, event_id: UUID, inscription_id: UUID, payment_id: UUID) -> PaymentsResponseSchema:
        conditions = [
            PaymentModel.event_id == event_id,
            PaymentModel.inscription_id == inscription_id,
            PaymentModel.id == payment_id
        ]
        res = await self._get_with_conditions(conditions)
        return PaymentsResponseSchema(
            id=res.id,
            event_id=res.event_id,
            inscription_id=res.inscription_id,
            status=res.status,
            works=res.works,
            fare_name=res.fare_name
        )

    async def get_payments_for_inscription(
            self,
            event_id: UUID,
            inscription_id: UUID,
            offset: int,
            limit: int
    ) -> list[PaymentsResponseSchema]:
        conditions = [PaymentModel.event_id == event_id, PaymentModel.inscription_id == inscription_id]
        return await self._get_payments(conditions, offset, limit)

    async def do_new_payment(self, event_id: UUID, inscription_id: UUID, payment_request: PaymentRequestSchema) -> UUID:
        new_payment = PaymentModel(
            **payment_request.model_dump(),
            event_id=event_id,
            inscription_id=inscription_id
        )
        return (await self._create(new_payment)).id

    async def update_status(self, event_id: UUID, payment_id: UUID, status: PaymentStatusSchema) -> bool:
        conditions = [PaymentModel.event_id == event_id, PaymentModel.id == payment_id]
        return await self._update_with_conditions(conditions, status)

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
