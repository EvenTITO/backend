from ..common import create_headers_organization


async def test_user_accept_organizer_invitation(
        client,
        event_creator_data,
        event_from_event_creator,
        organizer_id_from_event
):
    response = await client.patch(
        f"/events/{event_from_event_creator}/organizers/accept",
        headers=create_headers_organization(organizer_id_from_event, event_creator_data["id"])
    )
    assert response.status_code == 204

# TODO: agregar mas test de aceptar invitacion en casos donde no corresponde como:
#  ya fue aceptada
#  no existe la invitacion
#  ya expiro
#  no existe ese usuario
