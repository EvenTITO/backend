from app.schemas.members.member_schema import MemberRequestSchema
import pytest
from fastapi.encoders import jsonable_encoder

from app.schemas.events.schemas import EventRole
from ..commontest import create_headers


async def test_get_chairs_with_new_chair(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_member_request = MemberRequestSchema(
        email=create_user["email"],
        role=EventRole.CHAIR
    )
    response = await client.post(
        f"/events/{create_event_from_event_creator}/members",
        json=jsonable_encoder(create_member_request),
        headers=create_headers(create_event_creator["id"])
    )

    assert response.status_code == 201
    response = await client.get(
        f"/events/{create_event_from_event_creator}/chairs",
        headers=create_headers(create_event_creator["id"])
    )

    assert response.status_code == 200
    chair_list = response.json()
    assert len(chair_list) == 1
    unique_chair = chair_list[0]
    assert unique_chair['user_id'] == create_user['id']
    assert len(unique_chair['tracks']) == 0


async def test_get_chairs_empty(client, create_event_creator, create_event_from_event_creator):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/chairs",
        headers=create_headers(create_event_creator["id"])
    )

    assert response.status_code == 200
    chair_list = response.json()
    assert len(chair_list) == 0


@pytest.mark.skip(reason="TODO: obtener el chair por user_id con sus tracks si ese chair soy yo mismo y soy organizer")
async def test_get_chair_by_user_id_01():
    pass


@pytest.mark.skip(reason="TODO: obtener un chair por user_id con sus tracks si soy organizer")
async def test_get_chair_by_user_id_02():
    pass


@pytest.mark.skip(reason="TODO: (FALLO) tratar de obtener un chair por user_id si no soy organizer")
async def test_get_chair_by_user_id_03():
    pass


@pytest.mark.skip(reason="TODO: (FALLO) tratar de obtener un chair si no soy organizer pero ese user_id no es chair")
async def test_get_chair_by_user_id_04():
    pass


@pytest.mark.skip(reason="TODO:(FALLO) tratar de obtener chair si soy organizer pero ese user_id no existe como user")
async def test_get_chair_by_user_id_05():
    pass


@pytest.mark.skip(reason="TODO: obtener mis datos como chair si soy chair del evento")
async def test_get_chair_me_01():
    pass


@pytest.mark.skip(reason="TODO:(FALLO) obtener mis datos como chair si no soy chair del evento")
async def test_get_chair_me_02():
    pass
