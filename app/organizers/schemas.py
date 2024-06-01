from pydantic import BaseModel


class OrganizerRequestSchema(BaseModel):
    id_organizer: str


class OrganizerSchema(OrganizerRequestSchema):
    id_event: str
