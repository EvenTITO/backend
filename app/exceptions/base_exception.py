from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, errorcode: str, message: str, params: dict):
        super().__init__(status_code=status_code, detail={
            'errorcode': errorcode,
            'message': message,
            'params': params
        })
