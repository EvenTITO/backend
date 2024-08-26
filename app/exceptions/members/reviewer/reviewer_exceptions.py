from fastapi import HTTPException


class UserNotIsReviewer(HTTPException):
    def __init__(self, event_id, reviewer_id):
        self.status_code = 404
        self.detail = f"Not exist reviewer with user: {reviewer_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class AlreadyReviewerExist(HTTPException):
    def __init__(self, event_id, user_id, work_id):
        self.status_code = 403
        self.detail = f"Already reviewer user_id: {user_id} for work_id: {work_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)
