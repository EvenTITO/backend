from fastapi.encoders import jsonable_encoder
from ..commontest import create_headers


async def test_create_submission(client, create_user, create_event, create_work_from_user):
    event_id = create_event['id']
    submission = {}
    response = await client.put(
        f"/events/{event_id}/works/{create_work_from_user}/submissions/submit",
        json=jsonable_encoder(submission),
        headers=create_headers(create_user["id"])
    )
    assert response.status_code == 200, f'error: {response.json()}'
