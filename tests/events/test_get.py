from fastapi.encoders import jsonable_encoder
from app.events.model import EventStatus
from app.events.schemas import ModifyEventStatusSchema
from ..common import create_headers, EVENTS


async def test_get_event(client, event_data, user_data):
    response = await client.get(f"/events/{event_data['id']}",
                                headers=create_headers(user_data['id']))

    assert response.status_code == 200
    assert response.json()["title"] == event_data["title"]
    assert response.json()["status"] == EventStatus.WAITING_APPROVAL


async def test_get_event_not_exists_fails(client, user_data):
    id = "this-id-does-not-exist"
    response = await client.get(f"/events/{id}",
                                headers=create_headers(user_data['id']))

    assert response.status_code == 404
    # assert response.json()["detail"] == EVENT_NOT_FOUND


async def test_get_all_events_not_admin_error(
        client, all_events_data, user_data
):
    response = await client.get("/events/",
                                headers=create_headers(user_data['id']))
    assert response.status_code == 403


async def test_get_all_events_admin_gets_all(
        client, all_events_data, admin_data
):
    response = await client.get("/events/",
                                headers=create_headers(admin_data.id))
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_all_events_admin_query_waiting(
        client, all_events_data, admin_data
):
    status_update = ModifyEventStatusSchema(
        status=EventStatus.CREATED
    )
    response = await client.patch(
        f"/events/{all_events_data[0]}",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )

    response = await client.get(
        "/events/",
        headers=create_headers(admin_data.id),
        params={'status': EventStatus.WAITING_APPROVAL.value}
    )
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_all_events_non_admin_can_query_started(
        client, all_events_data, admin_data, user_data
):
    status_update = ModifyEventStatusSchema(
        status=EventStatus.STARTED
    )
    response = await client.patch(
        f"/events/{all_events_data[0]}",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )

    response = await client.get(
        "/events/",
        headers=create_headers(user_data['id']),
        params={'status': EventStatus.STARTED.value}
    )
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_events_non_admin_can_not_query_created(
        client, all_events_data, admin_data, user_data
):
    status_update = ModifyEventStatusSchema(
        status=EventStatus.STARTED
    )
    response = await client.patch(
        f"/events/{all_events_data[0]}",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )

    response = await client.get(
        "/events/",
        headers=create_headers(user_data['id']),
        params={'status': EventStatus.CREATED.value}
    )
    print(response.json())
    assert response.status_code == 403


async def test_get_all_events_query_by_title_same_title(
        client, all_events_data, admin_data
):
    response = await client.get(
        "/events/",
        headers=create_headers(admin_data.id),
        params={'search': EVENTS[0].title}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_events_query_by_title_contains(
        client, all_events_data, admin_data
):
    response = await client.get(
        "/events/",
        headers=create_headers(admin_data.id),
        params={'search': 'de'}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
