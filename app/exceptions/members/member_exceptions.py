from fastapi import HTTPException


class AlreadyMemberExist(HTTPException):
    def __init__(self, event_id, user_id, role):
        self.status_code = 403
        self.detail = f"Already member for user_id: {user_id} in event: {event_id} with role: {role}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class MemberRoleNotSupported(HTTPException):
    def __init__(self, role):
        self.status_code = 409
        self.detail = f"Member Role {role} not supported."
        super().__init__(status_code=self.status_code, detail=self.detail)
