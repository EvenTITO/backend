from fastapi import HTTPException


class AlreadyOrganizerExist(HTTPException):
    def __init__(self, event_id, user_id):
        self.status_code = 403
        self.detail = f"Already organizer for user_id: {user_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotIsOrganizer(HTTPException):
    def __init__(self, event_id, organizer_id):
        self.status_code = 404
        self.detail = f"Not exist organizer with user: {organizer_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class AtLeastOneOrganizer(HTTPException):
    def __init__(self, event_id, organizer_id):
        self.status_code = 403
        self.detail = f"There must be at least one organizer. Cannot delete {organizer_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)
