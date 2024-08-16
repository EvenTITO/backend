import pytest

from fastapi.encoders import jsonable_encoder
from ...commontest import create_headers, WORKS


@pytest.fixture(scope="function")
async def event_works(client, create_user, event_data):
    event_id = event_data['id']
    for work in WORKS:
        response = await client.post(
            f"/events/{event_id}/works",
            json=jsonable_encoder(work),
            headers=create_headers(create_user["id"])
        )
        work_id = response.json()
        work['id'] = work_id
    return WORKS
