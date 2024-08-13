from fastapi import HTTPException


class NotExistPendingOrganizerInvitation(HTTPException):
    def __init__(self, event_id, organizer_id):
        self.status_code = 404
        self.detail = f"Not exist organizer invitation with user_id: {organizer_id} in event: {event_id} pending"
        super().__init__(status_code=self.status_code, detail=self.detail)


class ExpiredOrganizerInvitation(HTTPException):
    def __init__(self, event_id, organizer_id):
        self.status_code = 403
        self.detail = f"Expired organizer invitation for user_id: {organizer_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotIsOrganizerAndNotExistInvitation(HTTPException):
    def __init__(self, event_id, organizer_id):
        self.status_code = 404
        self.detail = f"Not exist organizer or invitation with user: {organizer_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class AtLeastOneOrganizer(HTTPException):
    def __init__(self, event_id, organizer_id):
        self.status_code = 403
        self.detail = f"There must be at least one organizer. Cannot delete {organizer_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)
