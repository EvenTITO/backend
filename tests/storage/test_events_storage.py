from ..commontest import create_headers


async def test_get_event_contains_event_public_url(
    client,
    create_event,
    create_user
):
    response = await client.get(f"/events/{create_event['id']}/public",
                                headers=create_headers(create_user['id']))

    assert response.status_code == 200
    assert response.json()["title"] == create_event["title"]
    assert response.json()["media"][0]["name"] == 'main_image'
    assert len(response.json()["roles"]) == 0


async def test_get_event_upload_url_must_be_event_organizer(
    mock_storage,
    client,
    create_organizer,
    create_event_from_event_creator,
):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/upload_url/main_image",
        headers=create_headers(create_organizer)
    )

    assert response.status_code == 200
    assert response.json()["upload_url"] is not None


async def test_get_event_upload_url_not_organizer_fails(
    mock_storage,
    client,
    create_user,
    create_event_from_event_creator,
):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/upload_url/main_image",
        headers=create_headers(create_user['id'])
    )

    assert response.status_code == 403
