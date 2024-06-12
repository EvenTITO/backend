from app.events.schemas import ReviewSkeletonSchema
from fastapi.encoders import jsonable_encoder
from ..common import create_headers


async def test_patch_review_skeleton(client, admin_data, event_data):
    review_skeleton = ReviewSkeletonSchema(
        review_skeleton={
            "questions": [
                {
                    "first_question": "This is a normal question"
                },
                {
                    "multiple_choice": {
                        "question": "This is the question",
                        "answers": ["first", "second", "third"],
                        "can_choose_many": False,
                    }
                }
            ]
        }
    )
    response = await client.patch(
        f"/events/{event_data['id']}/review-skeleton",
        json=jsonable_encoder(review_skeleton),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204

    response = await client.get(
        f"/events/{event_data['id']}",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    first_question = \
        response.json()['review_skeleton']["questions"][0]["first_question"]

    assert first_question == \
        review_skeleton.review_skeleton["questions"][0]["first_question"]
