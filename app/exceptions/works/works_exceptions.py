from fastapi import HTTPException


class TitleAlreadyExists(HTTPException):
    def __init__(self, title, event_id):
        self.status_code = 409
        self.detail = f"Event title {title} already exists for the event {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class WorkNotFound(HTTPException):
    def __init__(self, event_id, work_id):
        self.status_code = 404
        self.detail = f"Work {work_id} in event {event_id} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotIsMyWork(HTTPException):
    def __init__(self, event_id, work_id):
        self.status_code = 404
        self.detail = f"Work {work_id} in event {event_id} not is yours"
        super().__init__(status_code=self.status_code, detail=self.detail)


class StatusNotAllowWorkUpdate(HTTPException):
    def __init__(self, status, work_id):
        self.status_code = 409
        self.detail = f"Status {status} on work {work_id} does not allow work update"
        super().__init__(status_code=self.status_code, detail=self.detail)


class CannotUpdateWorkAfterDeadlineDate(HTTPException):
    def __init__(self, deadline_date, work_id):
        self.status_code = 409
        self.detail = f"Submission deadline {deadline_date} for work {work_id} already passed"
        super().__init__(status_code=self.status_code, detail=self.detail)


class CannotCreateWorkAfterDeadlineDate(HTTPException):
    def __init__(self, deadline_date):
        self.status_code = 409
        self.detail = f"Event submission deadline {deadline_date} for create work already passed"
        super().__init__(status_code=self.status_code, detail=self.detail)


class TrackNotExistInEvent(HTTPException):
    def __init__(self, event_id, track):
        self.status_code = 409
        self.detail = f"Track: {track} not exist in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)
