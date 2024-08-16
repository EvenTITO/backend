from fastapi.encoders import jsonable_encoder

from app.database.models.work import WorkStates
from ..commontest import create_headers
from .test_create_work import USER_WORK


async def test_get_work_retrieves_work_data(client, create_user, create_event):
    event_id = create_event['id']
    response = await client.post(
        f"/events/{event_id}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    work_id = response.json()
    work_response = await client.get(
        f"/events/{event_id}/works/{work_id}",
        headers=create_headers(create_user["id"])
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


# async def test_create_work_deadline_date_is_event_deadline_date(client, create_user, create_event, create_many_works):
#     event_id = create_event['id']
#     work_id = create_many_works[0]['id']
#     get_work_resp = await client.get(
#         f"/events/{event_id}/works/{work_id}",
#         headers=create_headers(create_user["id"])
#     )
#     work_response = get_work_resp.json()
#     assert False
