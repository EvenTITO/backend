from fastapi import HTTPException


class AlreadyChairExist(HTTPException):
    def __init__(self, event_id, user_id):
        self.status_code = 403
        self.detail = f"Already chair for user_id: {user_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotIsChair(HTTPException):
    def __init__(self, event_id, chair_id):
        self.status_code = 404
        self.detail = f"Not exist chair or invitation with user: {chair_id} in event: {event_id}"
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidUpdateTrack(HTTPException):
    def __init__(self, event_id, new_track, tracks):
        self.status_code = 400
        self.detail = f"Invalid track: {new_track}. The available tracks in event: {event_id} are {tracks}."
        super().__init__(status_code=self.status_code, detail=self.detail)
