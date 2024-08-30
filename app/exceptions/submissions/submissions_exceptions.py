from fastapi import HTTPException


class SubmissionNotFound(HTTPException):
    def __init__(self, event_id, work_id):
        self.status_code = 404
        self.detail = f"Submission from Work {work_id} in event ${event_id} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)
