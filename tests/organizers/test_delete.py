

# def test_event_creator_can_remove_other_organizer(
#         client, organizer_id_from_event,
#         event_from_event_creator, event_creator_data
# ):
#     request = OrganizerRequestSchema(
#         id_organizer=organizer_id_from_event
#     )
#     response = client.delete(f"/organizers/{event_from_event_creator['id']}",
#                              json=jsonable_encoder(request),
#                              headers=create_headers(event_creator_data['id']))
#     assert response.status_code == 200


# def test_event_organizer_can_remove_other_event_organizer(
#         client, organizer_id_from_event,
#         event_from_event_creator, user_data
# ):
#     request = OrganizerRequestSchema(
#         id_organizer=user_data['id']
#     )
#     client.post(f"/organizers/{event_from_event_creator['id']}",
#                 json=jsonable_encoder(request),
#                 headers=create_headers(organizer_id_from_event))

#     response = client.delete(f"/organizers/{event_from_event_creator['id']}",
#                              json=jsonable_encoder(request),
#                              headers=create_headers(organizer_id_from_event))
#     assert response.status_code == 200


# def test_event_organizer_tries_remove_event_creator_fails(
#         client, organizer_id_from_event,
#         event_from_event_creator, event_creator_data
# ):
#     request = OrganizerRequestSchema(
#         id_organizer=event_creator_data['id']
#     )
#     response = client.delete(f"/organizers/{event_from_event_creator['id']}",
#                              json=jsonable_encoder(request),
#                              headers=create_headers(organizer_id_from_event))
#     assert response.status_code == 403


# def test_simple_user_tries_remove_organizer_fails(
#         client, organizer_id_from_event,
#         event_from_event_creator, user_data
# ):
#     request = OrganizerRequestSchema(
#         id_organizer=organizer_id_from_event
#     )
#     response = client.delete(f"/organizers/{event_from_event_creator['id']}",
#                              json=jsonable_encoder(request),
#                              headers=create_headers(user_data['id']))
#     assert response.status_code == 404
