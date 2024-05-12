from app.schemas.users import UserSchema
from ..common import client
from app.schemas.events import CreateEventSchema
from fastapi.encoders import jsonable_encoder
from app.models.event import EventType
from app.crud.events import CREATOR_NOT_EXISTS
from datetime import datetime


# ------------------------------- POST TESTS ------------------------------- #

event_creator = UserSchema(
    id="iuaealdasldanfasdlasd",
    name="Lio",
    surname="Messi",
    email="lio_messi@email.com"
)


def test_post_event():
    response = client.post("/users/", json=jsonable_encoder(event_creator))

    new_event = CreateEventSchema(
        title="Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
        creator_id=event_creator.id
    )
    response = client.post("/events/", json=jsonable_encoder(new_event))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data['id_event'] is not None


def test_post_event_invalid_creator():
    invalid_creator_event = CreateEventSchema(
        title="Another Event Title",
        start_date=datetime(2024, 9, 2),
        end_date=datetime(2024, 9, 3),
        description="This is a nice event",
        event_type=EventType.CONFERENCE,
        creator_id="bocaaaa"
    )

    response = client.post("/events/",
                           json=jsonable_encoder(invalid_creator_event))
    print(response.json())
    assert response.status_code == 404
    assert response.json()['detail'] == CREATOR_NOT_EXISTS


# def test_post_event_invalid_end_date():
#     end_date_in_the_past = CreateEventSchema(
#         title="Event Title",
#         start_date="2023-09-02",
#         end_date="2023-09-04",
#         description="This is a nice event",
#         event_type=EventType.CONFERENCE,
#         id_creator=event_creator.id
#     )
#     response = client.post("/events/",
#                            json=jsonable_encoder(end_date_in_the_past))
#     assert response.status_code == 422


# def test_post_event_invalid_dates():
#     end_date_before_start_date = CreateEventSchema(
#         title="Event Title",
#         start_date="2024-09-02",
#         end_date="2024-09-03",
#         description="This is a nice event",
#         event_type=EventType.CONFERENCE,
#         id_creator=event_creator.id
#     )
#     response = client.post("/events/",
#                            json=jsonable_encoder(end_date_before_start_date))
#     assert response.status_code == 422
