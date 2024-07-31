from app.schemas.events.review_skeleton.review_skeleton import ReviewScheletonQuestions, ReviewSkeletonSchema
from app.schemas.events.review_skeleton.simple_question import SimpleQuestion
from app.schemas.events.review_skeleton.multiples_choice_question import (
    MultipleChoiceQuestion
)
from fastapi.encoders import jsonable_encoder
from ..common import create_headers


async def test_put_review_skeleton(client, admin_data, event_data):
    first_question = 'This is a simple question that has a str answer'
    review_skeleton = ReviewSkeletonSchema(
        review_skeleton=ReviewScheletonQuestions(
            questions=[
                SimpleQuestion(
                    type_question='simple_question',
                    question=first_question
                ),
                MultipleChoiceQuestion(
                    type_question='multiple_choice',
                    question='This is the question',
                    options=['first answer', 'second answer', 'third answer'],
                    more_than_one_answer_allowed=False
                )
            ]
        )
    )
    response = await client.put(
        f"/events/{event_data['id']}/configuration/review-skeleton",
        json=jsonable_encoder(review_skeleton),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204

    response = await client.get(
        f"/events/{event_data['id']}/configuration/review-skeleton",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    print(response.json())
    assert response.json()["review_skeleton"]["questions"][0]["question"] == first_question
