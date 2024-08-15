import pytest

from ...commontest import create_headers


@pytest.fixture(scope="function")
async def inscription_data(client, user_data, event_data):
    event_id = event_data['id']
    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(user_data["id"])
    )
    inscriptor_id = response.json()
    return {'event_id': event_id, 'inscriptor_id': inscriptor_id}
