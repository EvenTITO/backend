# flake8: noqa
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
    track='chemistry',
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
