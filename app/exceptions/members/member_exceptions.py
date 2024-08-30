from fastapi import HTTPException


class AlreadyMemberExist(HTTPException):
    def __init__(self, event_id, user_id, role):
        self.status_code = 403
        self.detail = f"Already member for user_id: {user_id} in event: {event_id} with role: {role}"
        super().__init__(status_code=self.status_code, detail=self.detail)
