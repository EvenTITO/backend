from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


## EVENT TYPES
CONFERENCE = 'CONFERENCE'
TALK = 'TALK'

## STATUS
CREATED = 'CREATED'
STARTED = 'STARTED'

class EventSchema(BaseModel):
    id: str
    title: str = Field(min_length=2)
    creation_date: datetime
    start_date: datetime
    end_date: datetime
    description: str
    event_type: str
    status: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1234",
                    "title": "CONGRESO DE QUIMICA",
                    "creation_date": datetime.now(),
                    "start_date": datetime(2024, 8, 1),
                    "end_date": datetime(2024, 8, 3),
                    "description": "Evento en FIUBA",
                    "event_type": CONFERENCE,
                    "status": CREATED
                }
            ]
        }
    }
