from ..common import create_headers


async def test_get_event_configuration_organizer(
    client,
    user_data,
    event_creator_data,
    event_from_event_creator
):
    response = await client.get(
        f"/events/{event_from_event_creator}/configuration",
        headers=create_headers(event_creator_data["id"])
    )

    assert response.status_code == 200
