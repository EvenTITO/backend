from fastapi import HTTPException

from app.exceptions.base_exception import BaseHTTPException


class UserNotFound(BaseHTTPException):
    def __init__(self, user_id):
        super().__init__(
            404,
            'USER_NOT_FOUND',
            f"User {user_id} not found",
            {'user_id': user_id}
        )


class UserWithEmailNotFound(HTTPException):
    def __init__(self, email_user):
        self.status_code = 404
        self.detail = f"User with email {email_user} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmailAlreadyExists(HTTPException):
    def __init__(self, email_str):
        self.status_code = 409
        self.detail = f"Email {email_str} already exists"
        super().__init__(status_code=self.status_code, detail=self.detail)


class IdAlreadyExists(HTTPException):
    def __init__(self, id_str):
        self.status_code = 409
        self.detail = f"Id {id_str} already exists"
        super().__init__(status_code=self.status_code, detail=self.detail)


class CantRemoveLastAdmin(HTTPException):
    def __init__(self):
        self.status_code = 409
        self.detail = "System must have at least 1 admin"
        super().__init__(status_code=self.status_code, detail=self.detail)
