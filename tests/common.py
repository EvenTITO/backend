from app.schemas.users.user import UserSchema
from app.schemas.events.schemas import EventSchema
from app.models.event import EventType
from app.schemas.works.author import AuthorInformation
from app.schemas.works.work import WorkSchema


async def get_user_method(client, user_id):
    response = await client.get(
        f"/users/{user_id}",
        headers=create_headers(user_id)
    )

    return response.json()


def create_headers_organization(organization_user_id, event_id):
    return {
        "X-User-Id": organization_user_id,
        "event_id": event_id
    }


def create_headers(user_id):
    return {
        "X-User-Id": user_id
    }


USERS = [
    UserSchema(
        name="Lucia",
        lastname="Benitez",
        email="lbenitez@email.com",
    ),
    UserSchema(
        name="Marta",
        lastname="Benitez",
        email="mbenitez@email.com",
    ),
    UserSchema(
        name="Pedro",
        lastname="Benitez",
        email="pbenitez@email.com",
    )
]


EVENTS = [
    EventSchema(
        title="Conferencia de química",
        start_date="2024-09-02",
        end_date="2024-09-04",
        description="""
        Conferencia donde se tratará el tema de hidrocarburos
        """,
        event_type=EventType.CONFERENCE,
        location='Paseo Colon 850',
        tracks=['math', 'chemistry', 'phisics'],
    ),
    EventSchema(
        title="Maratón de proba",
        start_date="2024-08-01",
        end_date="2024-08-02",
        description="Abierta para todos los estudiantes" +
        "de la materia Probabilidad y Estadística",
        event_type=EventType.TALK,
        location='Paseo Colon 850',
        tracks=['math', 'chemistry', 'phisics'],
    ),
    EventSchema(
        title="Conferencia JIAFES",
        start_date="2024-08-01",
        end_date="2024-08-05",
        description="Nueva edición de la conferencia",
        event_type=EventType.CONFERENCE,
        location='Paseo Colon 850',
        tracks=['math', 'chemistry', 'phisics'],
    )
]


WORKS = [
    WorkSchema(
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
    ),
    WorkSchema(
        title=(
            'Aplicaciones de los Toros de Clifford en '
            'la Teoría de Códigos Correctores de Errores'
        ),
        track='math',
        abstract=(
            "Este trabajo explora los toros de Clifford y su aplicación en la "
            "teoría de códigos correctores de errores. Los toros de Clifford, "
            "con sus propiedades topológicas y geométricas únicas, permiten "
            "el diseño de códigos que mejoran la eficiencia y robustez en la "
            "detección y corrección de errores en sistemas de comunicación "
            "digital. Se presenta un marco teórico que aprovecha la simetría "
            "y periodicidad de estos toros para simplificar la codificación y "
            "decodificación, demostrando mejoras significativas en "
            "comparación con los métodos tradicionales."
        ),
        keywords=['math', 'topology', 'Clifford Torus', 'Complex Spaces'],
        authors=[
            AuthorInformation(
                full_name='Juan Sanchez',
                membership='FIUBA',
                mail='juansanchez@mail.com'
            ),
            AuthorInformation(
                full_name='Julian Altocapo',
                membership='Exactas',
                mail='julianaltocapo@mail.com'
            )
        ]
    )
]
