import pytest
from fastapi.encoders import jsonable_encoder

from app.schemas.events.schemas import EventRole
from app.schemas.members.chair_schema import ChairRequestSchema
from ..commontest import create_headers


@pytest.mark.skip(reason="TODO: agregar tracks luego de crear chair porque se crea por default sin tracks")
async def test_get_chairs_with_new_chair(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    request = ChairRequestSchema(
        email=create_user["email"],
        tracks=["futbol", "tenis"],
        role=EventRole.CHAIR
    )

    await client.post(f"/events/{create_event_from_event_creator}/members",
                      json=jsonable_encoder(request),
                      headers=create_headers(create_event_creator["id"]))

    response = await client.get(
        f"/events/{create_event_from_event_creator}/chairs",
        headers=create_headers(create_event_creator["id"])
    )

    assert response.status_code == 200
    chair_list = response.json()
    assert len(chair_list) == 1
    unique_chair = chair_list[0]
    assert unique_chair['user_id'] == create_user['id']
    assert unique_chair['role'] == "chair"
    for track in unique_chair['tracks']:
        assert track in ['futbol', 'tenis']


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
