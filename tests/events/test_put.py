from ..common import create_headers


def test_put_event(client, post_event):
    event_dict = post_event()
    event_dict['json']["title"] = "new event"
    event_dict['json']["end_date"] = "2024-09-05T00:00:00"

    response = client.put(
        f"/events/{event_dict['id_event']}",
        json=event_dict['json'],
        headers=create_headers(event_dict['id_creator'])
    )

    assert response.status_code == 204


def test_put_event_with_invalid_end_date_fails(
    client,
    post_event
):
    event_dict = post_event()
    event_dict['json']["title"] = "new event"
    # start_date is 2024-09-02
    event_dict['json']["end_date"] = "2024-09-01T00:00:00"

    response = client.put(
        f"/events/{event_dict['id_event']}",
        json=event_dict['json'],
        headers=create_headers(event_dict['id_creator'])
    )

    assert response.status_code == 400
