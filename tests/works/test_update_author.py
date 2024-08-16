from fastapi.encoders import jsonable_encoder
from ..commontest import create_headers
from .test_create_work import USER_WORK


async def test_get_work_author_can_update_his_work(client, create_user, create_event):
    event_id = create_event['id']
    response = await client.post(
        f"/events/{event_id}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    work_id = response.json()
    update_work = USER_WORK.model_copy()
    update_work.title = 'new work title'

    response = await client.put(
        f"/events/{event_id}/works/{work_id}",
        json=jsonable_encoder(update_work),
        headers=create_headers(create_user["id"])
    )

    assert response.status_code == 204

    work_response = await client.get(
        f"/events/{event_id}/works/{work_id}",
        headers=create_headers(create_user["id"])
    )
    work_get = work_response.json()
    assert work_response.status_code == 200

    assert work_get["title"] == update_work.title
