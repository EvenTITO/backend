from fastapi.encoders import jsonable_encoder
from datetime import datetime
from app.events.schemas import (
    DatesCompleteSchema,
    CustomDateSchema
)
from ..common import create_headers


async def test_put_dates_config(client, admin_data, event_data):
    dates = DatesCompleteSchema(
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        deadline_submission_date=datetime(2024, 8, 1),
        custom_dates=[
            CustomDateSchema(
                name='deadeline re submissions',
                description='can resubmit after the first review',
                value=datetime(2024, 8, 15)
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
        f"/events/{event_data['id']}/dates",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    dates_json_encoded = dates.model_dump(mode='json')
    assert response.json()["start_date"] == dates_json_encoded['start_date']
    assert response.json()["end_date"] == dates_json_encoded['end_date']
    assert response.json()["custom_dates"][0]['name'] == \
        dates.custom_dates[0].name
