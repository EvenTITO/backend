import pytest

from fastapi.encoders import jsonable_encoder
from app.schemas.members.member_schema import MemberRequestSchema
from app.schemas.users.user import UserSchema
from ...commontest import create_headers


@pytest.fixture(scope="function")
async def organizer_id_from_event(client, create_event_creator, create_event_from_event_creator):
    organizer = UserSchema(
        name="Martina",
        lastname="Rodriguez",
        email="mrodriguez@email.com",
    )
    organizer_id = "frlasdvpqqad08jd"
    await client.post(
        "/users",
        json=jsonable_encoder(organizer),
        headers=create_headers(organizer_id)
    )
    request = MemberRequestSchema(
        email=organizer.email
    )
    # invite organizer
    response = await client.post(f"/events/{create_event_from_event_creator}/organizers",
                                 json=jsonable_encoder(request),
                                 headers=create_headers(create_event_creator['id']))

    assert response.status_code == 201

    # accept organizer invite
    response = await client.patch(f"/events/{create_event_from_event_creator}/organizers/accept",
                                  headers=create_headers(organizer_id))
    assert response.status_code == 204
    return organizer_id
