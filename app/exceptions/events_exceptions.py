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


class OrganizerFound(HTTPException):
    def __init__(self, event_id, email):
        self.status_code = 409
        self.detail = f"Organizer with email: {email} in event: {event_id} already exists"
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidQueryEventNotCreatedNotAdmin(HTTPException):
    def __init__(self, status: EventStatus | None, role: UserRole):
        self.status_code = 409
        self.detail = f"Invalid query for status: {status} while having the role: {role}."
        super().__init__(status_code=self.status_code, detail=self.detail)
