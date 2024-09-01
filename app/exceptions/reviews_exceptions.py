from fastapi import HTTPException


class IsNotWorkRevisionPeriod(HTTPException):
    def __init__(self, event_id, work_id):
        self.status_code = 409
        self.detail = f"Cannot do review because is not work revision period for work: {work_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)
