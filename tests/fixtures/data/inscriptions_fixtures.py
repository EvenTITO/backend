import pytest
from fastapi.encoders import jsonable_encoder

from app.schemas.inscriptions.inscription import InscriptionRequestSchema
from ...commontest import create_headers


@pytest.fixture(scope="function")
async def create_inscription(client, create_user, create_event_started):
    new_inscription = InscriptionRequestSchema(
        roles=["ATTENDEE"],
        affiliation="Fiuba",
    )

    await client.post(
        f"/events/{create_event_started}/inscriptions",
        json=jsonable_encoder(new_inscription),
        headers=create_headers(create_user["id"])
    )
    return {'event_id': create_event_started, 'user_id': create_user["id"]}
