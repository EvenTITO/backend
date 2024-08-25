# flake8: noqa
import pytest
from fastapi.encoders import jsonable_encoder

from app.schemas.works.author import AuthorInformation
from app.schemas.works.work import WorkSchema
from ..commontest import create_headers

USER_WORK = WorkSchema(
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


async def test_create_work(client, create_user, create_event):
    event_id = create_event['id']
    response = await client.post(
        f"/events/{event_id}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )
    assert response.status_code == 201


@pytest.mark.skip(reason="TODO: el id del trabajo ahora es string y cambio la primary key, revisar")
async def test_create_work_two_works_different_events_same_work_id(client, create_user, create_many_events):
    """
    When a new work is created, it should have the id as the next id available (incremental).
    This increment should be for each event.
    """
    id_first_event = create_many_events[0]
    id_second_event = create_many_events[1]

    first_work_response = await client.post(
        f"/events/{id_first_event}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )

    second_work_response = await client.post(
        f"/events/{id_second_event}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )

    first_work_id_for_both_events = 1
    assert first_work_response.status_code == 201
    assert first_work_response.json() == first_work_id_for_both_events

    assert second_work_response.status_code == 201
    assert second_work_response.json() == first_work_id_for_both_events


async def test_create_two_works_same_title_same_event_fails(client, create_user, create_event):
    """
    When many works are created in the same event, they all should have a different incremental id.
    """
    event_id = create_event['id']

    response = await client.post(
        f"/events/{event_id}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )

    second_response = await client.post(
        f"/events/{event_id}/works",
        json=jsonable_encoder(USER_WORK),
        headers=create_headers(create_user["id"])
    )

    assert response.status_code == 201
    assert second_response.status_code == 409, "The second response should fail given that the title is repeated"
