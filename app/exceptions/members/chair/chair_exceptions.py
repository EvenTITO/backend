from fastapi import HTTPException


class ChairInvitationAlreadyExist(HTTPException):
    def __init__(self, event_id, email):
        self.status_code = 409
        self.detail = f"Chair with email: {email} in event: {event_id} has already been invited"
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotExistChairInvitation(HTTPException):
    def __init__(self, event_id, chair_id):
        self.status_code = 404
        self.detail = f"Not exist chair invitation with user_id: {chair_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class CannotUpdateChairInvitation(HTTPException):
    def __init__(self, event_id, chair_id):
        self.status_code = 403
        self.detail = f"Cannot update chair invitation for user_id: {chair_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)

