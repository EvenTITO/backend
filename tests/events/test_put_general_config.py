import pytest
from fastapi.encoders import jsonable_encoder

from ..commontest import create_headers


async def test_put_event(client, admin_data, create_event):
    update_create_event = create_event.copy()
    update_create_event["title"] = "new event"
    update_create_event["end_date"] = "2024-09-05T00:00:00"
    update_create_event["notification_mails"] = []
    event_id = update_create_event.pop('id')

    response = await client.put(
        f"/events/{event_id}/configuration/general",
        json=jsonable_encoder(update_create_event),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204


async def test_put_event_different_notif_mails(
        client,
        admin_data,
        create_event
):
    update_create_event = create_event.copy()
    update_create_event["title"] = "new event"
    update_create_event["end_date"] = "2024-09-05T00:00:00"
    added_mail = 'mateo@mail.com'
    update_create_event["notification_mails"] = [
        added_mail, 'someother@mail.com']
    event_id = update_create_event.pop('id')

    _ = await client.put(
        f"/events/{event_id}/configuration/general",
        json=jsonable_encoder(update_create_event),
        headers=create_headers(admin_data.id)
    )
    response = await client.get(
        f"/events/{event_id}/configuration",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    assert response.json()['notification_mails'][0] == added_mail


async def test_put_event_change_tracks(
        client,
        admin_data,
        create_event
):
    update_create_event = create_event.copy()
    update_create_event["title"] = "new event"
    new_tracks = ["first_track", "second_track"]
    update_create_event["tracks"] = new_tracks
    update_create_event["notification_mails"] = []
    event_id = update_create_event.pop('id')

    _ = await client.put(
        f"/events/{event_id}/configuration/general",
        json=jsonable_encoder(update_create_event),
        headers=create_headers(admin_data.id)
    )
    response = await client.get(
        f"/events/{event_id}/configuration",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    assert response.json()['tracks'][0] == new_tracks[0]
    assert response.json()['tracks'][1] == new_tracks[1]


async def test_put_many_changes(
        client,
        admin_data,
        create_event
):
    update_create_event = create_event.copy()
    update_create_event["title"] = "new event"
    new_tracks = ["first_track", "second_track"]
    update_create_event["tracks"] = new_tracks
    update_create_event["title"] = 'New Event Title'
    update_create_event["description"] = 'New Event Description'
    update_create_event["location"] = 'New Event Location'
    update_create_event["contact"] = 'New Event Contact Info'
    update_create_event["notification_mails"] = []
    event_id = update_create_event.pop('id')

    _ = await client.put(
        f"/events/{event_id}/configuration/general",
        json=jsonable_encoder(update_create_event),
        headers=create_headers(admin_data.id)
    )
    response = await client.get(
        f"/events/{event_id}/configuration",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    assert response.json()['tracks'][0] == new_tracks[0]
    assert response.json()['tracks'][1] == new_tracks[1]

    # the title and description do not change.
    assert response.json()['title'] == create_event["title"]
    assert response.json()['description'] == create_event["description"]

    assert response.json()['location'] == update_create_event["location"]
    assert response.json()['contact'] == update_create_event["contact"]


@pytest.mark.skip(reason="TODO: validar agregar tracks nuevos despues de startup servicio PUT /general")
async def test_add_tracks_1():
    pass


@pytest.mark.skip(reason="TODO: validar agregar tracks nuevos despues de startup servicio PUT /general/tracks")
async def test_add_tracks_2():
    pass


@pytest.mark.skip(reason="TODO: validar agregar tracks nuevos antes de startup servicio PUT /general/tracks")
async def test_add_tracks_3():
    pass
