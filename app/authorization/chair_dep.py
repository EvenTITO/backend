from typing import Annotated

from fastapi import Depends, HTTPException, Query

from app.authorization.caller_id_dep import CallerIdDep
from app.services.event_chairs.event_chairs_service_dep import EventChairServiceDep


class IsChair:
    async def __call__(self, caller_id: CallerIdDep, event_id: str, chair_service: EventChairServiceDep) -> bool:
        return await chair_service.is_chair(event_id, caller_id)


is_chair = IsChair()
IsChairDep = Annotated[bool, Depends(is_chair)]


class VerifyIsChair:
    async def __call__(self, is_event_chair: IsChairDep) -> None:
        if not is_event_chair:
            raise HTTPException(status_code=403)


verify_is_chair = VerifyIsChair()
ChairDep = Annotated[None, Depends(verify_is_chair)]


class IsTrackChair:
    async def __call__(
            self,
            caller_id: CallerIdDep,
            event_id: str,
            chair_service: EventChairServiceDep,
            track: str = Query(...)
    ) -> bool:
        if await chair_service.is_chair(event_id, caller_id):
            chair = await chair_service.get_chair(event_id, caller_id)
            return track in chair.tracks
        return False


is_track_chair = IsTrackChair()
IsTrackChairDep = Annotated[bool, Depends(is_track_chair)]


class VerifyIsTrackChair:
    async def __call__(self, is_event_track_chair: IsTrackChairDep) -> None:
        if not is_event_track_chair:
            raise HTTPException(status_code=403)


verify_is_track_chair = VerifyIsTrackChair()
TrackChairDep = Annotated[None, Depends(verify_is_track_chair)]