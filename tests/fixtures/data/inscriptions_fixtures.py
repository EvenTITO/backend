import pytest

from ...commontest import create_headers


@pytest.fixture(scope="function")
async def create_inscription(client, create_user, create_event):
    event_id = create_event['id']
    response = await client.post(
        f"/events/{event_id}/inscriptions",
        headers=create_headers(create_user["id"])
    )
    inscriptor_id = response.json()
    return {'event_id': event_id, 'inscriptor_id': inscriptor_id}
