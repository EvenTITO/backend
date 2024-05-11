from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class EVENT_TYPE(Enum):
    # TODO: ver todos los tipos
    CONFERENCE = 'CONFERENCE'
    TALK = 'TALK'


class STATUS(Enum):
    # TODO: ver todos los estados
    CREATED = 'CREATED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'


class EventSchema(BaseModel):
    id: str
    name: str
    creation_date: datetime
    start_date: datetime
    end_date: datetime
    description: str
    event_type: EVENT_TYPE
    status: STATUS

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1234",
                    "name": "CONGRESO DE QUIMICA",
                    "creation_date": datetime.now(),
                    "start_date": datetime(2024, 8, 1),
                    "end_date": datetime(2024, 8, 3),
                    "description": "Evento en FIUBA",
                    "event_type": EVENT_TYPE.CONFERENCE,
                    "status": STATUS.CREATED
                }
            ]
        }
    }