from fastapi.encoders import jsonable_encoder

from app.schemas.inscriptions.inscription import InscriptionRequestSchema
from ..commontest import create_headers
from ..fixtures.data.events_fixtures import create_many_events_started_with_emails


async def test_get_inscription(client, create_inscription, admin_data):
    event_id = create_inscription['event_id']
    response = await client.get(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    inscriptions = response.json()
    assert len(inscriptions) == 1
    assert (inscriptions[0]['user_id'] == create_inscription['user_id'])


async def test_user_inscribes_to_two_events(client, create_user, create_many_events_started):
    new_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE"],
        affiliation="Fiuba",
    )
    _ = await client.post(
        f"/events/{create_many_events_started_with_emails[0]}/inscriptions",
        json=jsonable_encoder(new_inscription),
        headers=create_headers(create_user['id'])
    )

    _ = await client.post(
        f"/events/{create_many_events_started_with_emails[1]}/inscriptions",
        json=jsonable_encoder(new_inscription),
        headers=create_headers(create_user['id'])
    )

    response = await client.get(
        "/events/my-events",
        headers=create_headers(create_user['id'])
    )

    assert response.status_code == 200

    inscriptions_response = response.json()
    inscripted_events = [create_many_events_started_with_emails[0], create_many_events_started_with_emails[1]]
    # assert len(inscriptions_response) == 2
    for inscription in inscriptions_response:
        assert inscription['id'] in inscripted_events
