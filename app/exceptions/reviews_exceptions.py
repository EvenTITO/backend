from fastapi import HTTPException


class IsNotWorkRevisionPeriod(HTTPException):
    def __init__(self, event_id, work_id):
        self.status_code = 409
        self.detail = f"Cannot do review because is not work revision period for work: {work_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class CannotPublishReviews(HTTPException):
    def __init__(self, event_id, work_id):
        self.status_code = 409
        self.detail = f"Cannot publish reviews because they dont pertain to the work: {work_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class AlreadyReviewExist(HTTPException):
    def __init__(self, event_id, work_id, submission_id):
        self.status_code = 409
        self.detail = (
            f"Cannot add review because it already exists. work: {work_id} "
            f"event: {event_id}; submission: {submission_id}"
        )
        super().__init__(status_code=self.status_code, detail=self.detail)
