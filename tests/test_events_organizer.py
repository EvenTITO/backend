from fastapi.encoders import jsonable_encoder
from app.organizers.crud import EVENT_ORGANIZER_NOT_FOUND
from app.organizers.schemas import OrganizerRequestSchema
from .common import create_headers


def test_event_creator_can_add_other_user_as_event_organizer(
        client, event_creator_data, event_from_event_creator, user_data
):
    request = OrganizerRequestSchema(
        id_organizer=user_data["id"]
    )
    response = client.post(f"/organizers/{event_from_event_creator['id']}",
                           json=jsonable_encoder(request),
                           headers=create_headers(event_creator_data["id"]))
    print(response.json())
    assert response.status_code == 200
    assert response.json()["id_organizer"] == user_data["id"]
    assert response.json()["id_event"] == event_from_event_creator["id"]


def test_event_organizer_can_add_other_user_as_event_organizer(
        client, organizer_id_from_event, event_from_event_creator, user_data):
    request = OrganizerRequestSchema(
        id_organizer=user_data["id"]
    )
    response = client.post(f"/organizers/{event_from_event_creator['id']}",
                           json=jsonable_encoder(request),
                           headers=create_headers(organizer_id_from_event))
    assert response.status_code == 200
    assert response.json()["id_organizer"] == user_data["id"]
    assert response.json()["id_event"] == event_from_event_creator["id"]


def test_simple_user_tries_add_organizer_fails(
        client, user_data
):
    request = OrganizerRequestSchema(
        id_organizer=user_data["id"]
    )
    response = client.post(f"/organizers/{user_data['id']}",
                           json=jsonable_encoder(request),
                           headers=create_headers(user_data['id']))
    assert response.status_code == 404
    assert response.json()['detail'] == EVENT_ORGANIZER_NOT_FOUND


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
