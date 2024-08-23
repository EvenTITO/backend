from typing import Annotated

from fastapi import Depends, HTTPException

from app.authorization.chair_dep import IsChairDep, IsTrackChairDep
from app.authorization.organizer_dep import IsOrganizerDep


class IsOrganizerOrChair:
    async def __call__(self, is_organizer: IsOrganizerDep, is_chair: IsChairDep) -> bool:
        return is_organizer or is_chair


is_organizer_or_chair = IsOrganizerOrChair()
IsOrganizerOrChairDep = Annotated[bool, Depends(is_organizer_or_chair)]


class VerifyIsOrganizerOrChair:
    async def __call__(self, is_event_organizer_or_chair: IsOrganizerOrChairDep) -> None:
        if not is_event_organizer_or_chair:
            raise HTTPException(status_code=403)


verify_is_organizer_or_chair = VerifyIsOrganizerOrChair()
OrganizerOrChairDep = Annotated[str, Depends(verify_is_organizer_or_chair)]


class IsOrganizerOrTrackChair:
    async def __call__(self, is_organizer: IsOrganizerDep, is_track_chair: IsTrackChairDep) -> bool:
        return is_organizer or is_track_chair


is_organizer_or_track_chair = IsOrganizerOrTrackChair()
IsOrganizerOrTrackChairDep = Annotated[bool, Depends(is_organizer_or_track_chair)]


class VerifyIsOrganizerOrTrackChair:
    async def __call__(self, is_organizer_or_event_track_chair: IsOrganizerOrTrackChairDep) -> None:
        if not is_organizer_or_event_track_chair:
            raise HTTPException(status_code=403)


verify_is_organizer_or_track_chair = VerifyIsOrganizerOrTrackChair()
OrganizerOrTracksChairDep = Annotated[None, Depends(verify_is_organizer_or_track_chair)]
