from fastapi import HTTPException


class UserNotIsReviewer(HTTPException):
    def __init__(self, event_id, reviewer_id):
        self.status_code = 404
        self.detail = f"Not exist reviewer with user: {reviewer_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)
