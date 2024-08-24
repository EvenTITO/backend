import pytest
from fastapi.encoders import jsonable_encoder

from app.schemas.events.schemas import DynamicTracksEventSchema, EventRole
from app.schemas.members.member_schema import MemberRequestSchema
from ..commontest import create_headers


async def test_creator_can_add_user_as_chair(
        client,
        create_event_creator,
        create_event_from_event_creator,
        create_user
):
    request = MemberRequestSchema(
        email=create_user["email"],
        role=EventRole.CHAIR
    )
    response = await client.post(
        f"/events/{create_event_from_event_creator}/members",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )
    assert response.status_code == 201
    assert response.json() == create_user["id"]


async def test_organizer_can_add_user_as_chair(client, create_organizer, create_event_from_event_creator, create_user):
    request = MemberRequestSchema(
        email=create_user["email"],
        role=EventRole.CHAIR
    )
    response = await client.post(
        f"events/{create_event_from_event_creator}/members",
        json=jsonable_encoder(request),
        headers=create_headers(create_organizer)
    )
    assert response.status_code == 201
    assert response.json() == create_user["id"]


@pytest.mark.skip(reason="TODO: agregar los test que validan agregar tracks de un evento a un chair")
async def test_add_tracks_1(
        client,
        create_event_creator,
        create_event_from_event_creator,
        create_event_chair
):
    add_tracks_request = DynamicTracksEventSchema(
        tracks=["futbol", "tenis"],
    )
    response = await client.put(
        f"/events/{create_event_from_event_creator}/chairs/{create_event_chair}/tracks",
        json=jsonable_encoder(add_tracks_request),
        headers=create_headers(create_event_creator["id"])
    )
    assert response.status_code == 400


async def test_add_tracks_that_dont_exists_in_event_raises_error(
        client,
        create_event_creator,
        create_event_from_event_creator,
        create_event_chair
):
    add_tracks_request = DynamicTracksEventSchema(
        tracks=["futbol", "tenis"],
    )
    response = await client.put(
        f"/events/{create_event_from_event_creator}/chairs/{create_event_chair}/tracks",
        json=jsonable_encoder(add_tracks_request),
        headers=create_headers(create_event_creator["id"])
    )
    assert response.status_code == 400


@pytest.mark.skip(reason="TODO: agregar los test que validan agregar tracks validos a un member que no es chair")
async def test_add_tracks_3():
    pass


@pytest.mark.skip(reason="TODO: agregar test que validen pisar tracks actuales con los nuevos")
async def test_add_tracks_4():
    pass


@pytest.mark.skip(reason="TODO: agregar test que validen pisar tracks actuales con lista vacia")
async def test_add_tracks_5():
    pass


@pytest.mark.skip(reason="TODO: agregar test que validen el delete de chair")
async def test_add_tracks_6():
    pass
