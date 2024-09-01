import datetime as datetime_library
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from freezegun import freeze_time

from app.schemas.events.review_skeleton.simple_question import SimpleAnswer
from app.schemas.members.reviewer_schema import ReviewerRequestSchema, ReviewerCreateRequestSchema
from app.schemas.works.review import ReviewCreateRequestSchema, ReviewDecision, ReviewAnswer
from ..commontest import create_headers
from ..works.test_create_work import USER_WORK


async def test_create_review_error_work_is_not_in_revision_yet(
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
        email=create_user['email'],
        review_deadline=datetime_library.date.today() + datetime_library.timedelta(days=10)
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer_1]
    )

    reviewer_response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert reviewer_response.status_code == 201

    answer = ReviewAnswer(answers=[
        SimpleAnswer(question="Comentarios", answer="Muy buen trabajo.", type_question='simple_question')
    ])
    review = ReviewCreateRequestSchema(
        status=ReviewDecision.APPROVED,
        review=answer
    )

    create_review_response = await client.post(
        f"/events/{create_event_from_event_creator}/works/{work_id}/reviews",
        json=jsonable_encoder(review),
        headers=create_headers(create_user['id'])
    )
    assert create_review_response.status_code == 409


async def test_create_review_error_work_has_no_submissions(
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

    new_reviewer = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user['email'],
        review_deadline=datetime_library.date.today() + datetime_library.timedelta(days=10)
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer]
    )

    reviewer_response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert reviewer_response.status_code == 201

    answer = ReviewAnswer(answers=[
        SimpleAnswer(question="Comentarios", answer="Muy buen trabajo.", type_question='simple_question')
    ])
    review = ReviewCreateRequestSchema(
        status=ReviewDecision.APPROVED,
        review=answer
    )
    with freeze_time(datetime.now() + datetime_library.timedelta(days=31)):
        create_review_response = await client.post(
            f"/events/{create_event_from_event_creator}/works/{work_id}/reviews",
            json=jsonable_encoder(review),
            headers=create_headers(create_user['id'])
        )

    assert create_review_response.status_code == 404


async def test_create_review_ok(
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

    submission_response = await client.put(
        f"/events/{create_event_from_event_creator}/works/{work_id}/submissions/submit",
        headers=create_headers(create_event_creator['id'])
    )
    assert submission_response.status_code == 201

    new_reviewer = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user['email'],
        review_deadline=datetime_library.date.today() + datetime_library.timedelta(days=10)
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer]
    )

    reviewer_response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert reviewer_response.status_code == 201

    answer = ReviewAnswer(answers=[
        SimpleAnswer(question="Comentarios", answer="Muy buen trabajo.", type_question='simple_question')
    ])
    review = ReviewCreateRequestSchema(
        status=ReviewDecision.APPROVED,
        review=answer
    )
    with freeze_time(datetime.now() + datetime_library.timedelta(days=31)):
        create_review_response = await client.post(
            f"/events/{create_event_from_event_creator}/works/{work_id}/reviews",
            json=jsonable_encoder(review),
            headers=create_headers(create_user['id'])
        )

    assert create_review_response.status_code == 201
    assert create_review_response.json()["upload_url"]["upload_url"] == "mocked-url-upload"
    assert create_review_response.json()["event_id"] == create_event_from_event_creator
    assert create_review_response.json()["work_id"] == work_id
    assert create_review_response.json()["reviewer_id"] == create_user['id']
    assert len(create_review_response.json()["review"]["answers"]) == 1
    assert create_review_response.json()["review"]["answers"][0]["question"] == "Comentarios"
    assert create_review_response.json()["review"]["answers"][0]["answer"] == "Muy buen trabajo."
    assert create_review_response.json()["review"]["answers"][0]["type_question"] == "simple_question"
    assert create_review_response.json()["status"] == ReviewDecision.APPROVED


async def test_update_review_ok(
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

    submission_response = await client.put(
        f"/events/{create_event_from_event_creator}/works/{work_id}/submissions/submit",
        headers=create_headers(create_event_creator['id'])
    )
    assert submission_response.status_code == 201

    new_reviewer = ReviewerRequestSchema(
        work_id=work_id,
        email=create_user['email'],
        review_deadline=datetime_library.date.today() + datetime_library.timedelta(days=10)
    )

    request = ReviewerCreateRequestSchema(
        reviewers=[new_reviewer]
    )

    reviewer_response = await client.post(
        f"/events/{create_event_from_event_creator}/reviewers",
        json=jsonable_encoder(request),
        headers=create_headers(create_event_creator['id'])
    )

    assert reviewer_response.status_code == 201

    answer = ReviewAnswer(
        answers=[SimpleAnswer(
            question="Comentarios",
            answer="Mejorar desarrollo, es demasiado técnico y difícil de leer. Revisar ortografía.",
            type_question='simple_question'
        )]
    )
    review = ReviewCreateRequestSchema(
        status=ReviewDecision.NOT_APPROVED,
        review=answer
    )
    with freeze_time(datetime.now() + datetime_library.timedelta(days=31)):
        create_review_response = await client.post(
            f"/events/{create_event_from_event_creator}/works/{work_id}/reviews",
            json=jsonable_encoder(review),
            headers=create_headers(create_user['id'])
        )

        assert create_review_response.status_code == 201
        create_review = create_review_response.json()
        assert create_review["upload_url"]["upload_url"] == "mocked-url-upload"
        assert create_review["event_id"] == create_event_from_event_creator
        assert create_review["work_id"] == work_id
        assert create_review["reviewer_id"] == create_user['id']
        assert len(create_review["review"]["answers"]) == 1
        assert create_review["review"]["answers"][0]["question"] == "Comentarios"
        assert (create_review["review"]["answers"][0]["answer"] ==
                "Mejorar desarrollo, es demasiado técnico y difícil de leer. Revisar ortografía.")
        assert create_review["review"]["answers"][0]["type_question"] == "simple_question"
        assert create_review["status"] == ReviewDecision.NOT_APPROVED

        new_answer = ReviewAnswer(answers=[
            SimpleAnswer(question="Comentarios", answer="Bien las correcciones. Aprobado", type_question='simple_question')
        ])
        new_review = ReviewCreateRequestSchema(
            status=ReviewDecision.APPROVED,
            review=new_answer
        )
        update_review_response = await client.put(
            f"/events/{create_event_from_event_creator}/works/{work_id}/reviews/{create_review['id']}",
            json=jsonable_encoder(new_review),
            headers=create_headers(create_user['id'])
        )

    assert update_review_response.status_code == 201
