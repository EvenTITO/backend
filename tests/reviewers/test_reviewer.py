from app.reviewers.schemas.reviewer import ReviewerSchema
from app.models.organizer import InvitationStatus
from fastapi.encoders import jsonable_encoder
from ..common import create_headers
from datetime import datetime, timedelta


async def test_create_reviewer_auto_invited_OK(client, event_data, admin_data):
    # Admin try to add reviewer(user_data) that he did not organize
    # event_data is created for Admin
    # user_data is not Admin
    str_tracks = "track1, track2, track3"
    reviewer_schema = ReviewerSchema(
        invitation_expiration_date=datetime.now()+timedelta(days=1),
        invitation_status=InvitationStatus.INVITED,
        tracks="track1, track2, track3"
    )

    response = await client.post(
        f"/events/{event_data['id']}/reviewers/{admin_data.id}",
        json=jsonable_encoder(reviewer_schema),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 201

    response_data = response.json()
    assert response_data is not None
    assert response_data['id_event'] == event_data['id']
    assert response_data['invitation_status'] == InvitationStatus.INVITED
    assert response_data['tracks'] == str_tracks
    assert response_data['invitation_expiration_date']\
        == str((datetime.now()+timedelta(days=1)).date())
    assert response_data['id_user'] == admin_data.id
    assert response_data['creation_date'] is not None


async def test_create_reviewer_not_organizer_FAIL(client, event_data,
                                                  admin_data, user_data):
    # Admin try to add reviewer(user_data) that he did not organize
    # event_data is created for Admin
    # user_data is not Admin
    str_tracks = "track1, track2, track3"
    reviewer_schema = ReviewerSchema(
        invitation_expiration_date=datetime(2024, 12, 31),
        invitation_status=InvitationStatus.INVITED,
        tracks=str_tracks
    )

    response = await client.post(
        f"/events/{event_data['id']}/reviewers/{admin_data.id}",
        json=jsonable_encoder(reviewer_schema),
        headers=create_headers(user_data['id'])
    )
    assert response.status_code == 403


# TODO: validar que el invitation_expiration_date > now()
# TODO: validar que el status sea valido
