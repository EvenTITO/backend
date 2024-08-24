import datetime

from fastapi.encoders import jsonable_encoder

from app.schemas.events.dates import DatesCompleteSchema, DateSchema, MandatoryDates
from tests.commontest import create_headers


async def add_complete_dates(client, event_id, creator_user_id):
    dates = DatesCompleteSchema(
        dates=[
            DateSchema(
                name=MandatoryDates.START_DATE,
                label='Fecha de Comienzo',
                description='Fecha de comienzo del evento.',
                is_mandatory=True,
                date=datetime.date.today() + datetime.timedelta(days=31),
                time=datetime.time(15, 30)
            ),
            DateSchema(
                name=MandatoryDates.END_DATE,
                label='Fecha de Finalización',
                description='Fecha de Finalización del evento.',
                is_mandatory=True,
                date=datetime.date.today() + datetime.timedelta(days=32),
                time=datetime.time(15, 30)
            ),
            DateSchema(
                name=MandatoryDates.SUBMISSION_DEADLINE_DATE,
                label='Fecha de envío de trabajos',
                description='Fecha límite de envío de trabajos.',
                is_mandatory=True,
                date=datetime.date.today() + datetime.timedelta(days=30),
                time=datetime.time(15, 30)
            )
        ]
    )

    response2 = await client.put(
        f"/events/{event_id}/configuration/dates",
        json=jsonable_encoder(dates),
        headers=create_headers(creator_user_id)
    )
    assert response2.status_code == 204
