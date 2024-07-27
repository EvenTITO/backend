from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

from app.schemas.event_dates import CustomDateSchema, DatesCompleteSchema
from app.schemas.works.author import AuthorInformation
from app.schemas.works.work import WorkSchema
from ..common import create_headers


user_work = WorkSchema(
    title=(
        'Comparación del Rendimiento de Curve25519, '
        'P-256 y Curvas de Edwards en Algoritmos '
        'de Criptografía Cuántica'
    ),
    track='cibersecurity',
    abstract='',
    keywords=['ciber', 'security'],
    authors=[
        AuthorInformation(
            full_name='Mateo Perez',
            membership='fiuba',
            mail='mail@mail.com'
        )
    ]
)


async def test_create_work(client, user_data, event_data):
    id_event = event_data['id']
    response = await client.post(
        f"/events/{id_event}/works",
        json=jsonable_encoder(user_work),
        headers=create_headers(user_data["id"])
    )
    first_work_id = 1
    assert response.status_code == 201
    assert response.json() == first_work_id


async def test_create_work_two_works_different_events_same_work_id(client, user_data, all_events_data):
    """
    When a new work is created, it should have the id as the next id available (incremental).
    This increment should be for each event.
    """
    id_first_event = all_events_data[0]
    id_second_event = all_events_data[1]

    first_work_response = await client.post(
        f"/events/{id_first_event}/works",
        json=jsonable_encoder(user_work),
        headers=create_headers(user_data["id"])
    )

    second_work_response = await client.post(
        f"/events/{id_second_event}/works",
        json=jsonable_encoder(user_work),
        headers=create_headers(user_data["id"])
    )

    first_work_id_for_both_events = 1
    assert first_work_response.status_code == 201
    assert first_work_response.json() == first_work_id_for_both_events

    assert second_work_response.status_code == 201
    assert second_work_response.json() == first_work_id_for_both_events


async def test_create_lots_works_in_same_event_should_have_incremental_ids(client, user_data, event_data):
    """
    When many works are created in the same event, they all should have a different incremental id.
    """
    id_event = event_data['id']
    number_works_to_create = 10
    ids_results = []

    async def create_work(work, i):
        work.title = work.title + str(i)
        response = await client.post(
            f"/events/{id_event}/works",
            json=jsonable_encoder(work),
            headers=create_headers(user_data["id"])
        )
        work_id = response.json()
        ids_results.append(work_id)

    for i in range(number_works_to_create):
        await create_work(user_work, i)

    for i in range(1, 1+number_works_to_create):
        assert i == ids_results[i-1]


async def test_create_two_works_same_title_same_event_fails(client, user_data, event_data):
    """
    When many works are created in the same event, they all should have a different incremental id.
    """
    id_event = event_data['id']

    response = await client.post(
        f"/events/{id_event}/works",
        json=jsonable_encoder(user_work),
        headers=create_headers(user_data["id"])
    )

    second_response = await client.post(
        f"/events/{id_event}/works",
        json=jsonable_encoder(user_work),
        headers=create_headers(user_data["id"])
    )

    assert response.status_code == 201
    assert second_response.status_code == 409, "The second response should fail given that the title is repeated"


async def test_create_work_deadline_date_is_event_deadline_date(client, user_data, event_data, admin_data):
    id_event = event_data['id']
    today = datetime.now()
    deadline = today+timedelta(days=10)
    dates = DatesCompleteSchema(
        start_date=today+timedelta(days=30),
        end_date=today+timedelta(days=31),
        deadline_submission_date=deadline,
        custom_dates=[
            CustomDateSchema(
                name='deadeline re submissions',
                description='can resubmit after the first review',
                value=today+timedelta(days=20)
            )
        ]
    )
    response = await client.put(
        f"/events/{event_data['id']}/configuration/dates",
        json=jsonable_encoder(dates),
        headers=create_headers(admin_data.id)
    )

    response = await client.post(
        f"/events/{id_event}/works",
        json=jsonable_encoder(user_work),
        headers=create_headers(user_data["id"])
    )

    assert response.status_code == 201
    assert False
