from fastapi.encoders import jsonable_encoder
import datetime
from app.schemas.events.dates import (
    DateSchema,
    DatesCompleteSchema,
    MandatoryDates
)
from ..common import create_headers


async def test_put_dates_config(client, admin_data, event_data):
    dates = DatesCompleteSchema(
        dates=[
            DateSchema(
                name=MandatoryDates.START_DATE,
                label='Fecha de Comienzo',
                description='Fecha de comienzo del evento.',
                is_mandatory=True
            ),
            DateSchema(
                name=MandatoryDates.END_DATE,
                label='Fecha de Finalización',
                description='Fecha de comienzo del evento.',
                is_mandatory=True
            ),
            DateSchema(
                name=MandatoryDates.SUBMISSION_DEADLINE_DATE,
                label='Fecha de envío de trabajos',
                description='Fecha límite de envío de trabajos.',
                is_mandatory=True
            ),
            DateSchema(
                name=None,
                label='deadeline re submissions',
                description='can resubmit after the first review.',
                is_mandatory=False,
                date=datetime.date.today()+datetime.timedelta(days=30),
                time=datetime.time(15, 30)
            )
        ]
    )
    response = await client.put(
        f"/events/{event_data['id']}/configuration/dates",
        json=jsonable_encoder(dates),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204

    response = await client.get(
        f"/events/{event_data['id']}/public",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    dates_response = response.json()["dates"]

    assert dates_response[0]["name"] == MandatoryDates.START_DATE
    assert dates_response[1]["name"] == MandatoryDates.END_DATE
    assert dates_response[2]["name"] == MandatoryDates.SUBMISSION_DEADLINE_DATE
