from fastapi import HTTPException


class TitleAlreadyExists(HTTPException):
    def __init__(self, title, event_id):
        self.status_code = 409
        self.detail = f"Event title {title} already exists for the event {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)
