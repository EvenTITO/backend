import pytest
from fastapi.encoders import jsonable_encoder

from app.exceptions.members.organizer.organizer_exceptions import NotExistPendingOrganizerInvitation
from app.schemas.members.member_schema import MemberRequestSchema
from app.schemas.users.user import UserSchema
from ..commontest import create_headers


async def test_user_accept_organizer_invitation(
        client,
        create_event_creator,
        create_event_from_event_creator,
        create_organizer,
):
    new_organizer = UserSchema(
        name="Fernando",
        lastname="Sinisi",
        email="fsinisi@email.com",
    )
    new_organizer_id = "122490u39nf93"
    await client.post(
        "/users",
        json=jsonable_encoder(new_organizer),
        headers=create_headers(new_organizer_id)
    )
    request = MemberRequestSchema(
        email=new_organizer.email
    )
    # invite organizer
    response = await client.post(f"/events/{create_event_from_event_creator}/organizers",
                                 json=jsonable_encoder(request),
                                 headers=create_headers(create_event_creator['id']))

    assert response.status_code == 201
    response = await client.patch(
        f"/events/{create_event_from_event_creator}/organizers/accept",
        headers=create_headers(new_organizer_id)
    )
    assert response.status_code == 204


async def send_invitation(client, event_id, user_id, email):
    request = MemberRequestSchema(
        email=email
    )
    return await client.post(
        f"/events/{event_id}/organizers",
        json=jsonable_encoder(request),
        headers=create_headers(user_id)
    )


async def accept_invitation(client, event_id, user_id):
    return await client.patch(
        f"/events/{event_id}/organizers/accept",
        headers=create_headers(user_id)
    )


async def test_accept_invitation_already_accepted_fails_invitation_not_found(
    client,
    create_event_creator,
    create_event_from_event_creator,
    create_user
):
    response = await send_invitation(
        client, create_event_from_event_creator, create_event_creator['id'], create_user['email']
    )
    assert response.status_code == 201
    response = await accept_invitation(client, create_event_from_event_creator, create_user['id'])
    assert response.status_code == 204
    response = await accept_invitation(client, create_event_from_event_creator, create_user['id'])
    assert response.status_code == 404
    print('Lo recibido es ', response.json()['detail'])
    assert response.json()['detail'] == \
        NotExistPendingOrganizerInvitation(create_event_from_event_creator, create_user['id']).detail


async def test_accept_invitation_no_invitation_given_not_exists(
    client,
    create_event_creator,
    create_event_from_event_creator,
    create_user
):
    response = await accept_invitation(client, create_event_from_event_creator, create_user['id'])
    assert response.status_code == 404
    assert response.json()['detail'] == \
        NotExistPendingOrganizerInvitation(create_event_from_event_creator, create_user['id']).detail


@pytest.mark.skip(reason="TODO")
async def test_accept_invitation_expired(
    client,
    create_event_creator,
    create_event_from_event_creator,
    create_user
):
    assert False


@pytest.mark.skip(reason="TODO")
async def test_accept_invitation_user_not_exists(
    client,
    create_event_creator,
    create_event_from_event_creator,
    create_user
):
    assert False
