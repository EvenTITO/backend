from fastapi.encoders import jsonable_encoder

from app.schemas.members.member_schema import MemberRequestSchema
from app.schemas.users.user import UserSchema
from ..commontest import create_headers


async def test_user_accept_organizer_invitation(
        client,
        event_creator_data,
        event_from_event_creator,
        organizer_id_from_event
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
    response = await client.post(f"/events/{event_from_event_creator}/organizers",
                                 json=jsonable_encoder(request),
                                 headers=create_headers(event_creator_data['id']))

    assert response.status_code == 201
    response = await client.patch(
        f"/events/{event_from_event_creator}/organizers/accept",
        headers=create_headers(new_organizer_id)
    )
    assert response.status_code == 204

# TODO: agregar mas test de aceptar invitacion en casos donde no corresponde como:
#  ya fue aceptada
#  no existe la invitacion
#  ya expiro
#  no existe ese usuario
