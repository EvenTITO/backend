from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self, user_id):
        self.status_code = 404
        self.detail = f"User {user_id} not found"
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


class EmailCantChange(HTTPException):
    def __init__(self, email1, email2):
        self.status_code = 409
        self.detail = f"Email must remain the same. {email1} != {email2}"
        super().__init__(status_code=self.status_code, detail=self.detail)
