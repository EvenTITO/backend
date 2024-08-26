from fastapi.encoders import jsonable_encoder

from app.schemas.members.reviewer_schema import ReviewerRequestSchema, ReviewerCreateRequestSchema
from ..commontest import create_headers
from ..works.test_create_work import USER_WORK


async def test_create_reviewers_ok(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator["id"])
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
        headers=create_headers(create_event_creator["id"])
    )

    assert response.status_code == 201


async def test_create_reviewers_already_exist_reviewer(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_1_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator["id"])
    )
    assert create_work_1_response.status_code == 201
    work_id_1 = create_work_1_response.json()

    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id_1,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )

    assert response.status_code == 201

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )

    assert response.status_code == 403


async def test_create_reviewers_by_work_id_invalid(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_1_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator["id"])
    )
    assert create_work_1_response.status_code == 201
    work_id_1 = create_work_1_response.json()

    new_reviewer_1 = ReviewerRequestSchema(
        work_id=work_id_1,
        email=create_user["email"],
        review_deadline="2024-06-07"
    )
    new_reviewer_2 = ReviewerRequestSchema(
        work_id="work_id_invalid",
        email=create_event_creator["email"],
        review_deadline="2024-06-07"
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1, new_reviewer_2]
    )

    response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator["id"])
    )

    assert response.status_code == 404


async def test_create_reviewers_without_permissions(
        client,
        create_user,
        create_event_creator,
        create_event_from_event_creator
):
    create_work_response = await client.post(
        f"/events/{create_event_from_event_creator}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_event_creator["id"])
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
        headers=create_headers(create_user["id"])
    )

    assert response.status_code == 403
