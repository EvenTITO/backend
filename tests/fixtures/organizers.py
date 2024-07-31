import pytest
from fastapi.encoders import jsonable_encoder

from app.schemas.members.member_schema import MemberRequestSchema
from ..common import create_headers


@pytest.fixture(scope="function")
def make_organizer_request(post_user):
    def make(id_user=None):
        if id_user is None:
            user_dict = post_user()
            id_user = user_dict['id']

        request = jsonable_encoder(MemberRequestSchema(
            id_organizer=id_user
        ))

        return {
            'id_user': id_user,
            'json': request
        }

    return make


@pytest.fixture(scope="function")
def make_new_organizer(post_event, make_organizer_request):
    def make(event_dict=None, id_user=None):
        if event_dict is None:
            event_dict = post_event()

        organizer_dict = make_organizer_request(id_user)

        return {
            'id_event': event_dict['id_event'],
            'id_creator': event_dict['id_creator'],
            'id_user': organizer_dict['id_user'],
            'json': organizer_dict['json']
        }

    return make


@pytest.fixture(scope="function")
def post_organizer(make_new_organizer, client):
    def post(event_dict=None, id_user=None):
        new_organizer_dict = make_new_organizer(event_dict, id_user)
        id_event = new_organizer_dict['id_event']
        id_creator = new_organizer_dict['id_creator']
        id_user = new_organizer_dict['id_user']
        request = new_organizer_dict['json']

        _ = client.post(
            f"/events/{id_event}/organizers",
            json=request,
            headers=create_headers(id_creator)
        )

        return {
            'id_event': id_event,
            'id_creator': id_creator,
            'id_organizer': id_user
        }

    return post


@pytest.fixture(scope="function")
def post_organizers(post_organizer, get_event):
    def post(n=1):
        organizers_dicts = []
        event = None
        for _ in range(n):
            if event is None:
                organizer_dict = post_organizer()
                id_event = organizer_dict['id_event']
                event = get_event(id_event).json()
            else:
                organizer_dict = post_organizer(event)

            organizers_dicts.append(organizer_dict)

        return organizers_dicts

    return post
