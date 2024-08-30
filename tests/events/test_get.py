import uuid
from app.database.models.user import UserRole
from app.exceptions.events_exceptions import EventNotFound, InvalidQueryEventNotCreatedNotAdmin
import pytest
from fastapi.encoders import jsonable_encoder
from app.database.models.event import EventStatus
from app.schemas.events.event_status import EventStatusSchema
from ..commontest import create_headers, EVENTS


async def test_get_event(client, create_event, create_user):
    response = await client.get(f"/events/{create_event['id']}/public",
                                headers=create_headers(create_user['id']))

    assert response.status_code == 200
    assert response.json()["title"] == create_event["title"]
    assert response.json()["status"] == EventStatus.CREATED  # The admin created it.
    assert len(response.json()["roles"]) == 0


async def test_get_event_not_exists_fails(client, create_user):
    this_id_does_not_exist = uuid.uuid4()
    response = await client.get(f"/events/{str(this_id_does_not_exist)}/public",
                                headers=create_headers(create_user['id']))

    assert response.status_code == 404
    assert response.json()['detail'] == EventNotFound(str(this_id_does_not_exist)).detail


async def test_get_event_not_exists_fails_with_422_if_not_uuid(client, create_user):
    this_id_does_not_exist = 'this-id-is-not-uuid'
    response = await client.get(f"/events/{this_id_does_not_exist}/public",
                                headers=create_headers(create_user['id']))

    assert response.status_code == 422


async def test_get_all_events_not_admin_error(
        client, create_many_events, create_user
):
    response = await client.get("/events/",
                                headers=create_headers(create_user['id']))
    assert response.status_code == 409
    assert response.json()['detail'] == \
        InvalidQueryEventNotCreatedNotAdmin(
            status=None,
            role=UserRole.DEFAULT.value
    ).detail


async def test_get_all_events_admin_gets_all(
        client, create_many_events, admin_data
):
    response = await client.get("/events/",
                                headers=create_headers(admin_data.id))
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_all_events_admin_status_waiting_approval_is_zero(
        client, create_many_events, admin_data
):
    status_update = EventStatusSchema(
        status=EventStatus.CREATED
    )
    response = await client.patch(
        f"/events/{create_many_events[0]}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )

    response = await client.get(
        "/events/",
        headers=create_headers(admin_data.id),
        params={'status': EventStatus.WAITING_APPROVAL.value}
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_get_all_events_non_admin_can_query_started(
        client, create_many_events, create_event_started, admin_data, create_user
):

    response = await client.get(
        "/events/",
        headers=create_headers(create_user['id']),
        params={'status': EventStatus.STARTED.value}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_events_non_admin_can_not_query_created(
        client, create_many_events, admin_data, create_user
):
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    response = await client.patch(
        f"/events/{create_many_events[0]}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )

    response = await client.get(
        "/events/",
        headers=create_headers(create_user['id']),
        params={'status': EventStatus.CREATED.value}
    )
    assert response.status_code == 409


async def test_get_all_events_query_by_title_same_title(
        client, create_many_events, admin_data
):
    response = await client.get(
        "/events/",
        headers=create_headers(admin_data.id),
        params={'search': EVENTS[0].title}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_events_query_by_title_contains(
        client, create_many_events, admin_data
):
    response = await client.get(
        "/events/",
        headers=create_headers(admin_data.id),
        params={'search': 'de'}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_all_events_public_is_status_created(client, create_event, admin_data):
    response = await client.get(
        "/events/",
        params={'status': EventStatus.STARTED.value},
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_events_public_is_status_created2(
        client, create_many_events_started_with_emails, admin_data
):

    n_events = len(create_many_events_started_with_emails)

    response = await client.get(
        "/events/",
        params={'status': EventStatus.STARTED.value},
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 200
    assert len(response.json()) == n_events


@pytest.mark.skip(reason="TODO: Write this code. Which date should we take? Or add a param for ordering?")
async def test_get_all_events_should_be_ordered_by_something():
    assert False
