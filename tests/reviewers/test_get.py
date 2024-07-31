from fastapi.encoders import jsonable_encoder
from ..common import create_headers
from app.schemas.members.member_schema import MemberRequestSchema

#todo cambiar a test de chairs
async def test_get_organizers_with_new_organizer(
    client,
    user_data,
    event_creator_data,
    event_from_event_creator
):
    request = MemberRequestSchema(
        email=user_data["email"]
    )
    _ = await client.post(f"/events/{event_from_event_creator}/organizers",
                          json=jsonable_encoder(request),
                          headers=create_headers(event_creator_data["id"]))

    response = await client.get(
        f"/events/{event_from_event_creator}/organizers",
        headers=create_headers(event_creator_data["id"])
    )

    assert response.status_code == 200

    organizers_list = response.json()
    assert len(organizers_list) == 2
    organizers_ids = [organizer['id_user']
                      for organizer in organizers_list]
    assert user_data['id'] in organizers_ids
