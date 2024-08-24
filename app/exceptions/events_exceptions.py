from fastapi import HTTPException

from app.database.models.event import EventStatus
from app.database.models.user import UserRole


class InvalidEventSameTitle(HTTPException):
    def __init__(self, title):
        self.status_code = 409
        self.detail = f"Title {title} already in use"
        super().__init__(status_code=self.status_code, detail=self.detail)


class EventNotFound(HTTPException):
    def __init__(self, event_id):
        self.status_code = 404
        self.detail = f"Event {event_id} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidQueryEventNotCreatedNotAdmin(HTTPException):
    def __init__(self, status: EventStatus | None, role: UserRole):
        self.status_code = 409
        self.detail = f"Invalid query for status: {status} while having the role: {role}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidEventConfiguration(HTTPException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Invalid event configuration for published"
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidCaller(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Invalid caller for operation"
        super().__init__(status_code=self.status_code, detail=self.detail)


class CannotUpdateTracksAfterEventStarts(HTTPException):
    def __init__(self, event_id: str):
        self.status_code = 409
        self.detail = f"Cannot update tracks in event:{event_id} after its started."
        super().__init__(status_code=self.status_code, detail=self.detail)
