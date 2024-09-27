import uuid

from fastapi.encoders import jsonable_encoder

from app.database.models.inscription import InscriptionStatus
from app.schemas.inscriptions.inscription import InscriptionRequestSchema
from app.schemas.payments.payment import PaymentRequestSchema
from ..commontest import create_headers


async def test_post_inscription(client, create_user, create_event_started):
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


async def test_post_inscription_duplicated(client, create_user, create_event_started):
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

    response = await client.post(
        f"/events/{create_event_started}/inscriptions",
        headers=create_headers(create_user["id"]),
        json=jsonable_encoder(new_inscription)
    )

    assert response.status_code == 409


async def test_post_inscription_without_event_fails(client, create_user):
    event_id_not_exists = uuid.uuid4()
    new_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE"],
        affiliation="Fiuba",
    )
    response = await client.post(
        f"/events/{event_id_not_exists}/inscriptions",
        headers=create_headers(create_user["id"]),
        json=jsonable_encoder(new_inscription)
    )
    assert response.status_code == 404


async def test_post_inscription_without_user_fails(client, create_event):
    event_id = create_event['id']
    user_id_not_exists = 'iduserdoesnotexists123456789'
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


async def test_update_inscription(client, create_user, create_event_started, create_speaker_inscription):
    update_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE"],
        affiliation="UTN",
    )

    inscription_id = create_speaker_inscription['id']

    response = await client.put(
        f"/events/{create_event_started}/inscriptions/{inscription_id}",
        headers=create_headers(create_user["id"]),
        json=jsonable_encoder(update_inscription)
    )
    assert response.status_code == 201
    assert response.json()['id'] == inscription_id
    assert response.json()['upload_url']['upload_url'] == 'mocked-url-upload'

    my_inscription_response = await client.get(
        f"/events/{create_event_started}/inscriptions/my-inscription",
        headers=create_headers(create_user["id"])
    )
    assert my_inscription_response.status_code == 200
    my_inscription = my_inscription_response.json()
    assert my_inscription['id'] == inscription_id
    assert my_inscription['user_id'] == create_user["id"]
    assert my_inscription['event_id'] == create_event_started
    assert my_inscription['status'] == InscriptionStatus.PENDING_APPROVAL
    assert len(my_inscription['roles']) == 1
    assert my_inscription['roles'][0] == "ATTENDEE"
    assert my_inscription['affiliation'] == "UTN"


async def test_pay_inscription(
        client,
        create_user,
        create_event_started,
        create_work_from_user,
        create_speaker_inscription
):
    pay_inscription = PaymentRequestSchema(
        fare_name="tarifa a pagar",
        works=[create_work_from_user],
    )
    inscription_id = create_speaker_inscription['id']

    response = await client.put(
        f"/events/{create_event_started}/inscriptions/{inscription_id}/pay",
        headers=create_headers(create_user["id"]),
        json=jsonable_encoder(pay_inscription)
    )
    assert response.status_code == 201
    assert response.json()['id'] is not None
    assert response.json()['upload_url']['upload_url'] == 'mocked-url-upload'
