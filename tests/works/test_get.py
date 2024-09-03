import datetime

from fastapi.encoders import jsonable_encoder

from app.database.models.work import WorkStates
from app.schemas.events.schemas import EventRole, DynamicTracksEventSchema
from app.schemas.members.member_schema import MemberRequestSchema
from app.schemas.users.user import UserSchema
from .test_create_work import USER_WORK
from ..commontest import create_headers


async def test_get_work_retrieves_work_data(client, create_user, create_event):
    event_id = create_event['id']
    response = await client.post(
        f"/events/{event_id}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    assert response.status_code == 201

    work_id = response.json()
    work_response = await client.get(
        f"/events/{event_id}/works/{work_id}",
        headers=create_headers(create_user["id"])
    )
    work_get = work_response.json()
    assert work_response.status_code == 200
    assert work_get["title"] == USER_WORK.title
    assert work_get["id"] == work_id
    assert work_get["state"] == WorkStates.SUBMITTED
    assert len(work_get["authors"]) == len(USER_WORK.authors)
    assert work_get["authors"][0]["membership"] == USER_WORK.authors[0].membership
    assert len(work_get["keywords"]) == len(USER_WORK.keywords)
    assert work_get["keywords"][0] == USER_WORK.keywords[0]
    assert work_get["abstract"] == USER_WORK.abstract
    assert work_get["track"] == USER_WORK.track


async def test_get_works_organizer(client, create_user, create_event_creator, create_event_from_event_creator):
    response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    assert response.status_code == 201

    work_id = response.json()
    works_response = await client.get(
        f"/events/{create_event_from_event_creator}/works",
        headers=create_headers(create_event_creator["id"])
    )

    assert works_response.status_code == 200
    works = works_response.json()
    assert len(works) == 1
    work = works[0]
    assert work["id"] == work_id
    assert work["title"] == USER_WORK.title
    assert work["track"] == USER_WORK.track
    assert work["abstract"] == USER_WORK.abstract
    assert work["state"] == WorkStates.SUBMITTED
    assert len(work["keywords"]) == 2
    assert set(work["keywords"]) == set(USER_WORK.keywords)
    assert (datetime.datetime.fromisoformat(work["deadline_date"]) ==
            datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=30),
                                      datetime.time(15, 30)))
    assert work["authors"][0]["membership"] == USER_WORK.authors[0].membership
    assert work["authors"][0]["full_name"] == USER_WORK.authors[0].full_name
    assert work["authors"][0]["mail"] == USER_WORK.authors[0].mail


async def test_get_works_organizer_with_track(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    work_response_1 = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    assert work_response_1.status_code == 201

    work_2 = USER_WORK.model_copy()
    work_2.title = 'nuevo titulo'
    work_2.track = 'math'

    work_response_2 = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(work_2),
        headers=create_headers(create_user["id"])
    )

    assert work_response_2.status_code == 201
    work_id_2 = work_response_2.json()

    all_works_response = await client.get(
        f"/events/{create_event_from_event_creator}/works",
        headers=create_headers(create_event_creator["id"])
    )

    assert all_works_response.status_code == 200
    works = all_works_response.json()
    assert len(works) == 2

    works_by_track_response = await client.get(
        f"/events/{create_event_from_event_creator}/works?track=math",
        headers=create_headers(create_event_creator["id"])
    )

    assert works_by_track_response.status_code == 200
    works_by_track = works_by_track_response.json()
    assert len(works_by_track) == 1
    work = works_by_track[0]
    assert work["id"] == work_id_2
    assert work["title"] == "nuevo titulo"
    assert work["track"] == "math"
    assert work["abstract"] == USER_WORK.abstract
    assert work["state"] == WorkStates.SUBMITTED
    assert len(work["keywords"]) == 2
    assert set(work["keywords"]) == set(USER_WORK.keywords)
    assert (datetime.datetime.fromisoformat(work["deadline_date"]) ==
            datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=30),
                                      datetime.time(15, 30)))
    assert work["authors"][0]["membership"] == USER_WORK.authors[0].membership
    assert work["authors"][0]["full_name"] == USER_WORK.authors[0].full_name
    assert work["authors"][0]["mail"] == USER_WORK.authors[0].mail


async def test_get_works_chair_with_track(client, create_user, create_event_creator, create_event_from_event_creator):
    other_user_id = "paoksncaokasdasdl12345678901"
    other_create_user = UserSchema(
        name="Angel",
        lastname="Di Maria",
        email="a.dimaria@email.com"
    )

    await client.post(
        "/users",
        json=jsonable_encoder(other_create_user),
        headers=create_headers(other_user_id)
    )

    request = MemberRequestSchema(
        email=other_create_user.email,
        role=EventRole.CHAIR
    )

    new_chair_response = await client.post(
        f"/events/{create_event_from_event_creator}/members",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )
    assert new_chair_response.status_code == 201

    add_tracks_request = DynamicTracksEventSchema(
        tracks=["math"],
    )
    response = await client.put(
        f"/events/{create_event_from_event_creator}/chairs/{other_user_id}/tracks",
        json=jsonable_encoder(add_tracks_request),
        headers=create_headers(create_event_creator["id"])
    )
    assert response.status_code == 204

    work_response_1 = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    assert work_response_1.status_code == 201

    work_2 = USER_WORK.model_copy()
    work_2.title = 'nuevo titulo'
    work_2.track = 'math'

    work_response_2 = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(work_2),
        headers=create_headers(create_user["id"])
    )

    assert work_response_2.status_code == 201
    work_id_2 = work_response_2.json()

    all_works_response = await client.get(
        f"/events/{create_event_from_event_creator}/works",
        headers=create_headers(create_event_creator["id"])
    )

    assert all_works_response.status_code == 200
    works = all_works_response.json()
    assert len(works) == 2

    works_by_track_response = await client.get(
        f"/events/{create_event_from_event_creator}/works?track=math",
        headers=create_headers(other_user_id)
    )

    assert works_by_track_response.status_code == 200
    works_by_track = works_by_track_response.json()
    assert len(works_by_track) == 1
    work = works_by_track[0]
    assert work["id"] == work_id_2
    assert work["title"] == "nuevo titulo"
    assert work["track"] == "math"
    assert work["abstract"] == USER_WORK.abstract
    assert work["state"] == WorkStates.SUBMITTED
    assert len(work["keywords"]) == 2
    assert set(work["keywords"]) == set(USER_WORK.keywords)
    assert (datetime.datetime.fromisoformat(work["deadline_date"]) ==
            datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=30),
                                      datetime.time(15, 30)))
    assert work["authors"][0]["membership"] == USER_WORK.authors[0].membership
    assert work["authors"][0]["full_name"] == USER_WORK.authors[0].full_name
    assert work["authors"][0]["mail"] == USER_WORK.authors[0].mail


async def test_get_works_chair_with_not_mine_track(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    other_user_id = "paoksncaokasdasdl12345678901"
    other_create_user = UserSchema(
        name="Angel",
        lastname="Di Maria",
        email="a.dimaria@email.com"
    )

    await client.post(
        "/users",
        json=jsonable_encoder(other_create_user),
        headers=create_headers(other_user_id)
    )

    request = MemberRequestSchema(
        email=other_create_user.email,
        role=EventRole.CHAIR
    )

    new_chair_response = await client.post(
        f"/events/{create_event_from_event_creator}/members",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )
    assert new_chair_response.status_code == 201

    add_tracks_request = DynamicTracksEventSchema(
        tracks=["math"],
    )
    response = await client.put(
        f"/events/{create_event_from_event_creator}/chairs/{other_user_id}/tracks",
        json=jsonable_encoder(add_tracks_request),
        headers=create_headers(create_event_creator["id"])
    )
    assert response.status_code == 204

    work_response_1 = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    assert work_response_1.status_code == 201

    work_2 = USER_WORK.model_copy()
    work_2.title = 'nuevo titulo'
    work_2.track = 'math'

    work_response_2 = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(work_2),
        headers=create_headers(create_user["id"])
    )

    assert work_response_2.status_code == 201

    all_works_response = await client.get(
        f"/events/{create_event_from_event_creator}/works",
        headers=create_headers(create_event_creator["id"])
    )

    assert all_works_response.status_code == 200
    works = all_works_response.json()
    assert len(works) == 2

    works_by_track_response = await client.get(
        f"/events/{create_event_from_event_creator}/works?track=chemistry",
        headers=create_headers(other_user_id)
    )

    assert works_by_track_response.status_code == 403


async def test_get_all_works_chair_non_authorized(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    other_user_id = "paoksncaokasdasdl12345678901"
    other_create_user = UserSchema(
        name="Angel",
        lastname="Di Maria",
        email="a.dimaria@email.com"
    )

    await client.post(
        "/users",
        json=jsonable_encoder(other_create_user),
        headers=create_headers(other_user_id)
    )

    request = MemberRequestSchema(
        email=other_create_user.email,
        role=EventRole.CHAIR
    )

    new_chair_response = await client.post(
        f"/events/{create_event_from_event_creator}/members",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )
    assert new_chair_response.status_code == 201

    work_response_1 = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    assert work_response_1.status_code == 201

    work_2 = USER_WORK.model_copy()
    work_2.title = 'nuevo titulo'
    work_2.track = 'math'

    work_response_2 = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(work_2),
        headers=create_headers(create_user["id"])
    )

    assert work_response_2.status_code == 201

    all_works_response = await client.get(
        f"/events/{create_event_from_event_creator}/works",
        headers=create_headers(create_event_creator["id"])
    )

    assert all_works_response.status_code == 200
    works = all_works_response.json()
    assert len(works) == 2

    works_by_track_response = await client.get(
        f"/events/{create_event_from_event_creator}/works",
        headers=create_headers(other_user_id)
    )

    assert works_by_track_response.status_code == 403