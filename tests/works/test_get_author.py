from fastapi.encoders import jsonable_encoder
from ..common import create_headers
from .test_create_work import USER_WORK


async def test_get_work_retrieves_work_data(client, user_data, event_data):
    id_event = event_data['id']
    response = await client.post(
        f"/events/{id_event}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(user_data["id"])
    )
    work_id = response.json()
    work_response = await client.get(
        f"/events/{id_event}/works/{work_id}",
        headers=create_headers(user_data["id"])
    )
    work_get = work_response.json()
    assert work_response.status_code == 200
    assert work_get["title"] == USER_WORK.title


# async def test_create_work_deadline_date_is_event_deadline_date(client, user_data, event_data, event_works):
#     id_event = event_data['id']
#     work_id = event_works[0]['id']
#     get_work_resp = await client.get(
#         f"/events/{id_event}/works/{work_id}",
#         headers=create_headers(user_data["id"])
#     )
#     work_response = get_work_resp.json()
#     assert False
