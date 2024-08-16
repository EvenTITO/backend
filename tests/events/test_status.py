from fastapi.encoders import jsonable_encoder

from app.database.models.event import EventStatus
from app.schemas.events.event_status import EventStatusSchema
from ..commontest import create_headers


async def test_event_created_has_waiting_approved_status(
        client, create_event, create_user
):
    response = await client.get(
        f"/events/{create_event['id']}/public",
        headers=create_headers(create_user['id'])
    )
    assert response.json()['status'] == EventStatus.WAITING_APPROVAL


async def test_event_created_organizer_cant_change_status(
        client, create_event, create_user
):
    status_update = EventStatusSchema(
        status=EventStatus.CREATED
    )
    response = await client.patch(
        f"/events/{create_event['id']}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(create_user['id'])
    )

    assert response.status_code == 403


async def test_organizer_can_change_status_to_started_after_created(
        client, create_event_from_event_creator, organizer_id_from_event, admin_data
):
    status_update = EventStatusSchema(
        status=EventStatus.CREATED
    )
    response = await client.patch(
        f"/events/{create_event_from_event_creator}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    response = await client.patch(
        f"/events/{create_event_from_event_creator}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(organizer_id_from_event)
    )

    assert response.status_code == 204


async def test_event_created_admin_can_change_status(
        client, create_event, admin_data
):
    status_update = EventStatusSchema(
        status=EventStatus.CREATED
    )
    response = await client.patch(
        f"/events/{create_event['id']}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204
    response = await client.get(
        f"/events/{create_event['id']}/public",
        headers=create_headers(admin_data.id)
    )
    assert response.json()['status'] == status_update.status
