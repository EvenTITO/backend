from fastapi import HTTPException


class ExpirationDateException(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Application expired"
        super().__init__(status_code=self.status_code, detail=self.detail)
