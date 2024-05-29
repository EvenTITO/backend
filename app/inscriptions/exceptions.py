from fastapi import HTTPException


class InscriptionAlreadyExists(HTTPException):
    def __init__(self, user_id, event_id):
        self.status_code = 409
        self.detail = f"Inscription from user: {user_id} "
        f"to event: {event_id} already exists."

        super().__init__(status_code=self.status_code, detail=self.detail)
