from app.events.crud import EVENT_NOT_FOUND


def test_get_event(client, post_event):
    event_dict = post_event()

    response = client.get(f"/events/{event_dict['id_event']}")
    print(event_dict)

    assert response.status_code == 200
    assert response.json()["title"] == event_dict['json']['title']


def test_get_event_not_exists_fails(client):
    id = "this-id-does-not-exist"
    response = client.get(f"/events/{id}")

    assert response.status_code == 404
    assert response.json()["detail"] == EVENT_NOT_FOUND


def test_get_all_events(client, post_events):
    N_EVENTS = 3
    _ = post_events(n=N_EVENTS)
    response = client.get("/events/")

    assert response.status_code == 200
    assert len(response.json()["events"]) == N_EVENTS
