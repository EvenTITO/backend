from fastapi.encoders import jsonable_encoder
from app.schemas.works.work import WorkUpdateAdministrationSchema
from app.schemas.works.talk import Talk
from ..commontest import create_headers


async def test_put_event_from_organizer(
    client,
    create_work_from_user,
    create_event_started,
    admin_data,
    create_speaker_inscription
):
    update = WorkUpdateAdministrationSchema(
        talk=Talk(date="2024-01-01 09:00:00", location='FIUBA, Av. Paseo Colon 850'),
        track="math"
    )
    response = await client.put(
        f"/events/{create_event_started}/works/{create_work_from_user}/administration",
        json=jsonable_encoder(update),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204
