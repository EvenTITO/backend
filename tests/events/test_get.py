from app.events.crud import EVENT_NOT_FOUND


def test_get_event(client, event_data):
    response = client.get(f"/events/{event_data['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == event_data["title"]


def test_get_event_not_exists_fails(client):
    id = "this-id-does-not-exist"
    response = client.get(f"/events/{id}")

    assert response.status_code == 404
    # assert response.json()["detail"] == EVENT_NOT_FOUND


def test_get_all_events(client, all_events_data):
    _ = all_events_data
    response = client.get("/events/")

    assert response.status_code == 200
    assert len(response.json()) == 3
