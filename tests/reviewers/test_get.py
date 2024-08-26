from fastapi.encoders import jsonable_encoder

from app.schemas.members.reviewer_schema import ReviewerRequestSchema, ReviewerCreateRequestSchema
from ..commontest import create_headers
from ..works.test_create_work import USER_WORK


async def test_get_reviewers_without_reviewers(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers",
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 200

    organizers_list = response.json()
    assert len(organizers_list) == 0


async def test_get_reviewers_ok(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )
    assert create_work_response.status_code == 201

    work_id = create_work_response.json()
    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )
    new_reviewer_2 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_event_creator["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1, new_reviewer_2]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 200

    reviewers_list = get_response.json()
    assert len(reviewers_list) == 2
    assert work_id in reviewers_list[0]["work_ids"]
    assert work_id in reviewers_list[1]["work_ids"]
    assert reviewers_list[0]["event_id"] == create_event_from_event_creator
    assert reviewers_list[1]["event_id"] == create_event_from_event_creator
    assert reviewers_list[0]["user_id"] == create_user['id']
    assert reviewers_list[1]["user_id"] == create_event_creator['id']
    assert reviewers_list[0]["user"]["email"] == create_user["email"]
    assert reviewers_list[1]["user"]["email"] == create_event_creator["email"]


async def test_get_reviewers_without_permissions(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers",
        headers=create_headers(create_user['id'])
    )

    assert response.status_code == 403


async def test_get_reviewers_by_work_id_ok(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_1_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )
    assert create_work_1_response.status_code == 201
    work_id_1 = create_work_1_response.json()

    new_work = USER_WORK.model_copy()
    new_work.title = 'new work title'

    create_work_2_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(new_work),
        headers=create_headers(create_event_creator['id'])
    )
    assert create_work_2_response.status_code == 201
    work_id_2 = create_work_2_response.json()

    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id_1,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )
    new_reviewer_2 = ReviewerRequestSchema(
        work_id=work_id_1,
        email=create_event_creator["email"],
        review_deadline="2024-06-07"
    )

    new_reviewer_3 = ReviewerRequestSchema(
        work_id=work_id_2,
        email=create_user["email"],
        review_deadline="2024-06-14"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1, new_reviewer_2, new_reviewer_3]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers?work_id={work_id_2}",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 200

    reviewers_list = get_response.json()
    assert len(reviewers_list) == 1
    assert work_id_1 not in reviewers_list[0]["work_ids"]
    assert work_id_2 in reviewers_list[0]["work_ids"]
    assert reviewers_list[0]["event_id"] == create_event_from_event_creator
    assert reviewers_list[0]["user_id"] == create_user['id']
    assert reviewers_list[0]["user"]["email"] == create_user["email"]


async def test_get_reviewers_by_work_id_invalid_return_empty_list(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_1_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )
    assert create_work_1_response.status_code == 201
    work_id_1 = create_work_1_response.json()

    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id_1,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )
    new_reviewer_2 = ReviewerRequestSchema(
        work_id=work_id_1,
        email=create_event_creator["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1, new_reviewer_2]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers?work_id=a17d7848-180c-4ab7-8eea-35c41bb78533",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 200
    reviewers = get_response.json()
    assert len(reviewers) == 0


async def test_get_reviewers_by_work_id_without_reviewers(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers?work_id=a1111111-180c-4ab7-8eea-35c41bb78533",
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 200

    organizers_list = response.json()
    assert len(organizers_list) == 0


async def test_get_reviewers_by_work_id_without_permissions(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers?work_id=4",
        headers=create_headers(create_user['id'])
    )

    assert response.status_code == 403


async def test_get_reviewer__by_user_id_without_permissions(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers/{create_user['id']}",
        headers=create_headers(create_user['id'])
    )

    assert response.status_code == 403


async def test_get_reviewer_by_user_id_without_reviewers(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers/{create_user['id']}",
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 404


async def test_get_reviewer__by_user_id_ok(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )
    assert create_work_response.status_code == 201

    work_id = create_work_response.json()
    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )
    new_reviewer_2 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_event_creator["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1, new_reviewer_2]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers/{create_user['id']}",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 200

    reviewer = get_response.json()
    assert work_id in reviewer["work_ids"]
    assert reviewer["event_id"] == create_event_from_event_creator
    assert reviewer["user_id"] == create_user['id']
    assert reviewer["user"]["email"] == create_user["email"]


async def test_get_reviewer_by_user_id_invalid_userid_not_uid(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )
    assert create_work_response.status_code == 201

    work_id = create_work_response.json()
    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )
    new_reviewer_2 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_event_creator["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1, new_reviewer_2]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers/user_id_invalid",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 422


async def test_get_reviewer_by_user_id_invalid_userid(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )
    assert create_work_response.status_code == 201

    work_id = create_work_response.json()
    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers/{create_event_creator['id']}",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 404


async def test_get_reviewer_by_user_id_not_reviewer_user_id(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )
    assert create_work_response.status_code == 201

    work_id = create_work_response.json()
    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/reviewers/{create_event_creator['id']}",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 404


async def test_get_reviewer_by_work_id_and_user_id_ok(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )

    assert create_work_response.status_code == 201

    work_id = create_work_response.json()
    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )
    new_reviewer_2 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_event_creator["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1, new_reviewer_2]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/works/{work_id}/reviewers/{create_user['id']}",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 200

    reviewer = get_response.json()
    assert reviewer["work_id"] == work_id
    assert reviewer["event_id"] == create_event_from_event_creator
    assert reviewer["user_id"] == create_user['id']
    assert reviewer["review_deadline"] == "2024-06-07"
    assert reviewer["user"]["email"] == create_user["email"]


async def test_get_reviewer_by_work_id_and_user_id_invalid_user_id(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator['id'])
    )

    assert create_work_response.status_code == 201

    work_id = create_work_response.json()
    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )
    new_reviewer_2 = ReviewerRequestSchema(
        work_id=work_id,
        email=create_event_creator["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1, new_reviewer_2]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert response.status_code == 201

    get_response = await client.get(
        f"/events/{create_event_from_event_creator}/works/{work_id}/reviewers/user_id_invalid",
        headers=create_headers(create_event_creator['id'])
    )

    assert get_response.status_code == 422