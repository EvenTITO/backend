from fastapi.encoders import jsonable_encoder
from app.database.models.event import EventStatus
from app.schemas.events.event_status import EventStatusSchema
from ..commontest import create_headers, EVENTS


async def test_get_event(client, event_data, create_user):
    response = await client.get(f"/events/{event_data['id']}/public",
                                headers=create_headers(create_user['id']))

    assert response.status_code == 200
    assert response.json()["title"] == event_data["title"]
    assert response.json()["status"] == EventStatus.WAITING_APPROVAL
    assert len(response.json()["roles"]) == 0


async def test_get_event_not_exists_fails(client, create_user):
    id = "this-id-does-not-exist"
    response = await client.get(f"/events/{id}/public",
                                headers=create_headers(create_user['id']))

    assert response.status_code == 404
    # assert response.json()["detail"] == EVENT_NOT_FOUND


async def test_get_all_events_not_admin_error(
        client, all_events_data, create_user
):
    response = await client.get("/events/",
                                headers=create_headers(create_user['id']))
    assert response.status_code == 400


async def test_get_all_events_admin_gets_all(
        client, all_events_data, admin_data
):
    response = await client.get("/events/",
                                headers=create_headers(admin_data.id))
    assert response.status_code == 200
    assert len(response.json()) == 3

# TODO: reveer!
# async def test_get_all_events_admin_status_waiting_approval_is_zero(
#         client, all_events_data, admin_data
# ):
#     status_update = EventStatusSchema(
#         status=EventStatus.CREATED
#     )
#     response = await client.patch(
#         f"/events/{all_events_data[0]}/status",
#         json=jsonable_encoder(status_update),
#         headers=create_headers(admin_data.id)
#     )

#     response = await client.get(
#         "/events/",
#         headers=create_headers(admin_data.id),
#         params={'status': EventStatus.WAITING_APPROVAL.value}
#     )
#     print(response.json())
#     assert response.status_code == 200
#     assert len(response.json()) == 0


async def test_get_all_events_non_admin_can_query_started(
        client, all_events_data, admin_data, create_user
):
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    response = await client.patch(
        f"/events/{all_events_data[0]}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )

    response = await client.get(
        "/events/",
        headers=create_headers(create_user['id']),
        params={'status': EventStatus.STARTED.value}
    )
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_events_non_admin_can_not_query_created(
        client, all_events_data, admin_data, create_user
):
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    response = await client.patch(
        f"/events/{all_events_data[0]}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )

    response = await client.get(
        "/events/",
        headers=create_headers(create_user['id']),
        params={'status': EventStatus.CREATED.value}
    )
    print(response.json())
    assert response.status_code == 400


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


async def test_get_all_events_public_is_status_created(
        client, event_started, admin_data
):
    response = await client.get(
        "/events/",
        params={'status': EventStatus.STARTED.value},
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_all_events_public_is_status_created2(
        client, all_events_data, admin_data
):
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    n_events = len(all_events_data)

    for event_id in all_events_data:
        await client.patch(
            f"/events/{event_id}/status",
            json=jsonable_encoder(status_update),
            headers=create_headers(admin_data.id)
        )

    response = await client.get(
        "/events/",
        params={'status': EventStatus.STARTED.value},
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 200
    assert len(response.json()) == n_events
