from fastapi.encoders import jsonable_encoder

from app.models.work import WorkStates
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
    assert work_get["id"] == work_id
    assert work_get["state"] == WorkStates.SUBMITTED
    assert len(work_get["authors"]) == len(USER_WORK.authors)
    assert work_get["authors"][0]["membership"] == USER_WORK.authors[0].membership
    assert len(work_get["keywords"]) == len(USER_WORK.keywords)
    assert work_get["keywords"][0] == USER_WORK.keywords[0]
    assert work_get["abstract"] == USER_WORK.abstract
    assert work_get["track"] == USER_WORK.track


# async def test_create_work_deadline_date_is_event_deadline_date(client, user_data, event_data, event_works):
#     id_event = event_data['id']
#     work_id = event_works[0]['id']
#     get_work_resp = await client.get(
#         f"/events/{id_event}/works/{work_id}",
#         headers=create_headers(user_data["id"])
#     )
#     work_response = get_work_resp.json()
#     assert False
