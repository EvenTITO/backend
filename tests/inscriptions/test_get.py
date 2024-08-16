from ..commontest import create_headers


async def test_get_inscription(client, create_inscription, admin_data):
    event_id = create_inscription['event_id']
    response = await client.get(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    inscriptions = response.json()
    assert len(inscriptions) == 1
    assert (inscriptions[0]['inscriptor_id'] ==
            create_inscription['inscriptor_id'])


async def test_user_inscribes_to_two_events(
        client, create_user, create_many_events
):
    _ = await client.post(
        f"/events/{create_many_events[0]}/inscriptions",
        headers=create_headers(create_user['id'])
    )

    _ = await client.post(
        f"/events/{create_many_events[1]}/inscriptions",
        headers=create_headers(create_user['id'])
    )

    response = await client.get(
        "/events/my-events",
        headers=create_headers(create_user['id'])
    )

    assert response.status_code == 200

    inscriptions_response = response.json()
    inscripted_events = [create_many_events[0], create_many_events[1]]
    assert len(inscriptions_response) == 2
    for inscription in inscriptions_response:
        assert inscription['id'] in inscripted_events
