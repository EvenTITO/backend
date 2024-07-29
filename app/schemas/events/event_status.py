from app.database.models.event import EventStatus


from pydantic import BaseModel, Field


class EventStatusSchema(BaseModel):
    status: EventStatus = Field(examples=[EventStatus.WAITING_APPROVAL])
