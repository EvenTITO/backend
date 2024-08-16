# from fastapi.encoders import jsonable_encoder
# from app.organizers.schemas import OrganizerRequestSchema
# from ..common import create_headers


# async def test_event_creator_can_remove_other_organizer(
#         client, organizer_id_from_event,
#         create_event_from_event_creator, create_event_creator
# ):
#     response = await client.delete(f"/events/{create_event_from_event_creator}"
#                                    f"/organizers/{organizer_id_from_event}",
#                                    headers=create_headers(create_event_creator['id']))
#     assert response.status_code == 204


# async def test_event_organizer_can_remove_other_event_organizer(
#         client, organizer_id_from_event,
#         create_event_from_event_creator, create_user
# ):
#     request = OrganizerRequestSchema(
#         organizer_id=create_user['id']
#     )
#     await client.post(f"/events/{create_event_from_event_creator}/organizers",
#                       json=jsonable_encoder(request),
#                       headers=create_headers(organizer_id_from_event))

#     response = await client.delete(f"/events/{create_event_from_event_creator}"
#                                    f"/organizers/{create_user['id']}",
#                                    headers=create_headers(organizer_id_from_event))
#     assert response.status_code == 204


# async def test_event_organizer_tries_remove_event_creator_fails(
#         client, organizer_id_from_event,
#         create_event_from_event_creator, create_event_creator
# ):
#     response = await client.delete(f"/events/{create_event_from_event_creator}"
#                                    f"/organizers/{create_event_creator}",
#                                    headers=create_headers(organizer_id_from_event))
#     assert response.status_code == 404


# async def test_simple_user_tries_remove_organizer_fails(
#         client, organizer_id_from_event,
#         create_event_from_event_creator, create_user
# ):
#     response = await client.delete(f"/events/{create_event_from_event_creator}"
#                                    f"/organizers/{organizer_id_from_event}",
#                                    headers=create_headers(create_user["id"]))

#     assert response.status_code == 404
