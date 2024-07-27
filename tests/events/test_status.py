from fastapi.encoders import jsonable_encoder

from app.models.event import EventStatus
from app.schemas.events.schemas import EventStatusSchema
from ..common import create_headers


async def test_event_created_has_waiting_approved_status(
        client, event_data, user_data
):
    response = await client.get(
        f"/events/{event_data['id']}/public",
        headers=create_headers(user_data['id'])
    )
    assert response.json()['status'] == EventStatus.WAITING_APPROVAL


async def test_event_created_organizer_cant_change_status(
        client, event_data, user_data
):
    status_update = EventStatusSchema(
        status=EventStatus.CREATED
    )
    response = await client.patch(
        f"/events/{event_data['id']}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 403


async def test_event_created_admin_can_change_status(
        client, event_data, admin_data
):
    status_update = EventStatusSchema(
        status=EventStatus.CREATED
    )
    response = await client.patch(
        f"/events/{event_data['id']}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204
    response = await client.get(
        f"/events/{event_data['id']}/public",
        headers=create_headers(admin_data.id)
    )
    assert response.json()['status'] == status_update.status
