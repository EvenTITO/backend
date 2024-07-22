from .mocks import mock_storage_functions
from ..common import create_headers


async def test_get_event_contains_event_public_url(
    client,
    event_data,
    user_data
):
    response = await client.get(f"/events/{event_data['id']}/public",
                                headers=create_headers(user_data['id']))

    assert response.status_code == 200
    assert response.json()["title"] == event_data["title"]
    assert response.json()["media"][0]["name"] == 'main_image_url'
    assert len(response.json()["roles"]) == 0


async def test_get_event_upload_url_must_be_event_organizer(
    client,
    organizer_id_from_event,
    event_from_event_creator,
    mocker,
):
    mock_storage_functions(mocker)
    response = await client.get(
        f"events/{event_from_event_creator}/upload_url/main_image",
        headers=create_headers(organizer_id_from_event)
    )

    assert response.json()["upload_url"] is not None
