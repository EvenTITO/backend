# from ..common import create_headers


# async def test_create_work_deadline_date_is_event_deadline_date(client, user_data, event_data, event_works):
#     id_event = event_data['id']
#     work_id = event_works[0]['id']
#     get_work_resp = await client.get(
#         f"/events/{id_event}/works/{work_id}",
#         headers=create_headers(user_data["id"])
#     )
#     work_response = get_work_resp.json()
#     assert False
