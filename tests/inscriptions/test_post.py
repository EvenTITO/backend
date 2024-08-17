from fastapi.encoders import jsonable_encoder

from app.schemas.inscriptions.inscription import InscriptionRequestSchema
from ..commontest import create_headers


async def test_post_inscription(client, mock_storage, create_user, create_event_started):
    new_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE"],
        affiliation="Fiuba",
    )

    response = await client.post(
        f"/events/{create_event_started}/inscriptions",
        headers=create_headers(create_user["id"]),
        json=jsonable_encoder(new_inscription)
    )
    assert response.status_code == 201
    assert response.json()['user_id'] == create_user['id']
    assert response.json()['roles'][0] == "ATTENDEE"


async def test_post_inscription_without_event_fails(client, create_user):
    event_id = "event-does-not-exists"
    new_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE"],
        affiliation="Fiuba",
    )
    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(create_user["id"]),
        json=jsonable_encoder(new_inscription)
    )
    assert response.status_code == 404


async def test_post_inscription_without_user_fails(client, create_event):
    event_id = create_event['id']
    user_id_not_exists = 'id-user-does-not-exists'
    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(user_id_not_exists)
    )
    assert response.status_code == 404


async def test_post_inscription_in_event_not_started(client, create_user, create_event):
    new_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE"],
        affiliation="Fiuba",
    )
    event_id = create_event['id']
    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(create_user["id"]),
        json=jsonable_encoder(new_inscription)
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "The event " + event_id + (" has not started."
                                                                   " The current event status is CREATED")
