from fastapi.encoders import jsonable_encoder

from app.submissions.schemas.author import AuthorInformation
from app.submissions.schemas.work import WorkSchema
from ..common import create_headers


async def test_create_work(client, user_data, event_data):
    id_event = event_data['id']
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

    response = await client.post(
        f"/events/{id_event}/works",
        json=jsonable_encoder(user_work),
        headers=create_headers(user_data["id"])
    )
    first_work_id = 1
    assert response.status_code == 201
    assert response.json() == first_work_id
