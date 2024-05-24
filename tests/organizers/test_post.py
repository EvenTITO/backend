from fastapi.encoders import jsonable_encoder
from app.organizers.crud import EVENT_ORGANIZER_NOT_FOUND
from app.organizers.schemas import OrganizerRequestSchema
from ..common import create_headers


def test_event_creator_can_add_other_user_as_event_organizer(
    client,
    make_new_organizer
):
    new_organizer_dict = make_new_organizer()
    id_event = new_organizer_dict['id_event']
    id_creator = new_organizer_dict['id_creator']
    id_user = new_organizer_dict['id_user']
    request = new_organizer_dict['json']

    response = client.post(
        f"/events/{id_event}/organizers",
        json=request,
        headers=create_headers(id_creator)
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json() == id_user


def test_event_organizer_can_add_other_user_as_event_organizer(
    client,
    post_organizer,
    make_organizer_request
):
    organizer_dict = post_organizer()
    user_dict = make_organizer_request()

    response = client.post(
        f"/events/{organizer_dict['id_event']}/organizers",
        json=user_dict['json'],
        headers=create_headers(organizer_dict['id_organizer'])
    )

    assert response.status_code == 201
    assert response.json() == user_dict['id_user']


def test_simple_user_tries_add_organizer_fails(
    client,
    make_organizer_request
):
    user_dict = make_organizer_request()

    response = client.post(
        f"/events/{user_dict['id_user']}/organizers",
        json=user_dict['json'],
        headers=create_headers(user_dict['id_user'])
    )

    assert response.status_code == 404
    assert response.json()['detail'] == EVENT_ORGANIZER_NOT_FOUND
