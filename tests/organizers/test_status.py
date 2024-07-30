from app.database.models.organizer import InvitationStatus
from fastapi.encoders import jsonable_encoder
from app.schemas.members.organizers.organizer_schema import ModifyInvitationStatusSchema
from ..common import create_headers_organization


async def test_event_creator_can_add_other_user_as_event_organizer(
        client, event_creator_data, event_from_event_creator,
        organizer_id_from_event
):
    request = ModifyInvitationStatusSchema(
        invitation_status=InvitationStatus.ACCEPTED)
    response = await client.patch(
        f"/events/{event_from_event_creator}/organizers",
        json=jsonable_encoder(request),
        headers=create_headers_organization(organizer_id_from_event,
                                            event_creator_data["id"])
    )
    print(response.json())
    assert response.status_code == 200

# TODO: add more test for patch and event status & expiration date
