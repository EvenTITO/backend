from fastapi import HTTPException


class InscriptionAlreadyExists(HTTPException):
    def __init__(self, event_id, user_id):
        self.status_code = 409
        self.detail = f"Inscription from user: {user_id} "
        f"to event: {event_id} already exists."

        super().__init__(status_code=self.status_code, detail=self.detail)


class EventNotStarted(HTTPException):
    def __init__(self, event_id, event_status):
        self.status_code = 409
        self.detail = (
            f"The event {event_id} has not started."
            f" The current event status is {event_status}"
        )
        super().__init__(status_code=self.status_code, detail=self.detail)


class InscriptionNotFound(HTTPException):
    def __init__(self, event_id, inscription_id):
        self.status_code = 404
        self.detail = f"Inscription {inscription_id} in event {event_id} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class MyInscriptionNotFound(HTTPException):
    def __init__(self, event_id):
        self.status_code = 404
        self.detail = f"You dont have inscription  in event {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)
