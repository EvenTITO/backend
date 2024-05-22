from app.users.schemas import UserSchema
from app.events.schemas import EventSchema
from app.events.model import EventType


def get_user(client, user_id):
    response = client.get(
        f"/users/{user_id}",
        headers=create_headers(user_id)
    )

    return response.json()


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
        event_type=EventType.CONFERENCE
    ),
    EventSchema(
        title="Maratón de proba",
        start_date="2024-08-01",
        end_date="2024-08-02",
        description="Abierta para todos los estudiantes" +
        "de la materia Probabilidad y Estadística",
        event_type=EventType.TALK
    ),
    EventSchema(
        title="Conferencia JIAFES",
        start_date="2024-08-01",
        end_date="2024-08-05",
        description="Nueva edición de la conferencia",
        event_type=EventType.CONFERENCE
    )
]
