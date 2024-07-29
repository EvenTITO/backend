# flake8: noqa
import pytest
from app.events.model import EventType
from app.events.schemas import EventSchema
from fastapi.encoders import jsonable_encoder
import randomname
from ..common import create_headers


@pytest.fixture(scope="function")
def make_event(make_event_creator):
    def create_random_event(id_creator=None, start_date=None, end_date=None):
        if id_creator is None:
            creator_dict = make_event_creator()
            id_creator = creator_dict['id']

        if start_date is None:
            start_date = "2024-09-02"
            end_date = "2024-09-04"

        new_event = EventSchema(
            title=randomname.get_name(),
            start_date=start_date,
            end_date=end_date,
            description=randomname.get_name(),
            event_type=EventType.CONFERENCE
        )

        return {
            'id_creator': id_creator,
            'json': jsonable_encoder(new_event)
        }

    return create_random_event


@pytest.fixture(scope="function")
def post_event(make_event, client):
    def post(id_creator=None, start_date=None, end_date=None):
        event_dict = make_event(id_creator, start_date, end_date)

        response_post = client.post(
            f"/events",
            json=event_dict['json'],
            headers=create_headers(event_dict['id_creator'])
        )

        event_dict['id_event'] = response_post.json()

        return event_dict

    return post


@pytest.fixture(scope="function")
def post_events(post_event):
    def post(n=1):
        events_dicts = []
        for _ in range(n):
            events_dicts.append(post_event())

        return events_dicts

    return post


@pytest.fixture(scope="function")
def get_event(client):
    def get(id_event):
        return client.get(f"/events/{id_event}")

    return get
