import pytest

from fastapi.encoders import jsonable_encoder
from app.database.models.event import EventStatus
from app.schemas.events.event_status import EventStatusSchema
from .commontest import WORKS, create_headers

from .fixtures.tests_configuration_fixtures import *  # noqa: F401, F403
from .fixtures.storage_mock_fixtures import *  # noqa: F401, F403
from .fixtures.application_setup_fixtures import *  # noqa: F401, F403
from .fixtures.data.users_fixtures import *  # noqa: F401, F403
from .fixtures.data.event_creator_fixtures import *  # noqa: F401, F403
from .fixtures.data.event_fixtures import *  # noqa: F401, F403
from .fixtures.data.inscriptions_fixtures import *  # noqa: F401, F403
from .fixtures.data.organizer_fixtures import *  # noqa: F401, F403


@pytest.fixture(scope="function")
async def event_started(client, event_data, admin_data):
    status_update = EventStatusSchema(
        status=EventStatus.STARTED
    )
    await client.patch(
        f"/events/{event_data['id']}/status",
        json=jsonable_encoder(status_update),
        headers=create_headers(admin_data.id)
    )
    return event_data['id']


@pytest.fixture(scope="function")
async def event_works(client, user_data, event_data):
    event_id = event_data['id']
    for work in WORKS:
        response = await client.post(
            f"/events/{event_id}/works",
            json=jsonable_encoder(work),
            headers=create_headers(user_data["id"])
        )
        work_id = response.json()
        work['id'] = work_id
    return WORKS
