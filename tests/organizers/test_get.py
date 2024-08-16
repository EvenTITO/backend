from fastapi.encoders import jsonable_encoder
from ..commontest import create_headers
from app.schemas.members.member_schema import MemberRequestSchema


async def test_get_organizers_with_new_organizer(
    client,
    create_user,
    event_creator_data,
    event_from_event_creator
):
    request = MemberRequestSchema(
        email=create_user["email"]
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
    organizers_ids = [organizer['user_id'] for organizer in organizers_list]
    assert create_user['id'] in organizers_ids
