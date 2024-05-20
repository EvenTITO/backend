from pydantic import BaseModel, ConfigDict
from typing import List


class OrganizerRequestSchema(BaseModel):
    id_organizer: str


class OrganizerSchema(OrganizerRequestSchema):
    id_event: str
