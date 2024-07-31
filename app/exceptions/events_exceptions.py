from fastapi import HTTPException


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
