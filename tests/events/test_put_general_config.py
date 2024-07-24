from fastapi.encoders import jsonable_encoder
from ..common import create_headers


async def test_put_event(client, admin_data, event_data):
    update_event_data = event_data.copy()
    update_event_data["title"] = "new event"
    update_event_data["end_date"] = "2024-09-05T00:00:00"
    update_event_data["notification_mails"] = []
    id_event = update_event_data.pop('id')

    response = await client.put(
        f"/events/{id_event}/general",
        json=jsonable_encoder(update_event_data),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204


async def test_put_event_with_invalid_end_date_fails(
    client,
    admin_data,
    event_data
):
    update_event_data = event_data.copy()
    # start_date = "2024-09-02"
    update_event_data["notification_mails"] = []
    update_event_data["end_date"] = "2024-08-05T00:00:00"
    id_event = update_event_data.pop('id')
    response = await client.put(
        f"/events/{id_event}/general",
        json=jsonable_encoder(update_event_data),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 422


async def test_put_event_different_notif_mails(
    client,
    admin_data,
    event_data
):
    update_event_data = event_data.copy()
    update_event_data["title"] = "new event"
    update_event_data["end_date"] = "2024-09-05T00:00:00"
    added_mail = 'mateo@mail.com'
    update_event_data["notification_mails"] = [
        added_mail, 'someother@mail.com']
    id_event = update_event_data.pop('id')

    _ = await client.put(
        f"/events/{id_event}/general",
        json=jsonable_encoder(update_event_data),
        headers=create_headers(admin_data.id)
    )
    response = await client.get(
        f"/events/{id_event}/configuration",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    assert response.json()['notification_mails'][0] == added_mail


async def test_put_event_change_tracks(
    client,
    admin_data,
    event_data
):
    update_event_data = event_data.copy()
    update_event_data["title"] = "new event"
    new_tracks = ["first_track", "second_track"]
    update_event_data["tracks"] = new_tracks
    update_event_data["notification_mails"] = []
    id_event = update_event_data.pop('id')

    _ = await client.put(
        f"/events/{id_event}/general",
        json=jsonable_encoder(update_event_data),
        headers=create_headers(admin_data.id)
    )
    response = await client.get(
        f"/events/{id_event}/configuration",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    assert response.json()['tracks'][0] == new_tracks[0]
    assert response.json()['tracks'][1] == new_tracks[1]


async def test_put_many_changes(
    client,
    admin_data,
    event_data
):
    update_event_data = event_data.copy()
    update_event_data["title"] = "new event"
    new_tracks = ["first_track", "second_track"]
    update_event_data["tracks"] = new_tracks
    update_event_data["title"] = 'New Event Title'
    update_event_data["description"] = 'New Event Description'
    update_event_data["location"] = 'New Event Location'
    update_event_data["contact"] = 'New Event Contact Info'
    update_event_data["notification_mails"] = []
    id_event = update_event_data.pop('id')

    _ = await client.put(
        f"/events/{id_event}/general",
        json=jsonable_encoder(update_event_data),
        headers=create_headers(admin_data.id)
    )
    response = await client.get(
        f"/events/{id_event}/configuration",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    print(response.json())
    assert response.json()['tracks'][0] == new_tracks[0]
    assert response.json()['tracks'][1] == new_tracks[1]
    assert response.json()['title'] == event_data["title"]
    assert response.json()['description'] == event_data["description"]
    assert response.json()['location'] == update_event_data["location"]
    assert response.json()['contact'] == update_event_data["contact"]
