from ..commontest import create_headers


async def test_post_inscription(client, create_user, create_event):
    event_id = create_event['id']
    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(create_user["id"])
    )
    assert response.status_code == 201
    assert response.json() == create_user['id']


async def test_post_inscription_without_event_fails(
        client,
        create_user
):
    event_id = "event-does-not-exists"

    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(create_user["id"])
    )
    assert response.status_code == 404
    # assert response.json()["detail"] == EVENT_NOT_FOUND


async def test_post_inscription_without_user_fails(client, create_event):
    event_id = create_event['id']
    user_id_not_exists = 'id-user-does-not-exists'
    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(user_id_not_exists)
    )
    assert response.status_code == 404
    # assert response.json()["detail"] == USER_NOT_FOUNT
