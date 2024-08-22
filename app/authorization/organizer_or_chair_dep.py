from typing import Annotated

from fastapi import Depends, HTTPException, Query

from app.authorization.caller_id_dep import CallerIdDep
from app.services.event_chairs.event_chairs_service_dep import EventChairServiceDep
from app.services.event_organizers.event_organizers_service_dep import EventOrganizersServiceDep
from app.services.works.works_service_dep import WorksServiceDep


class OrganizerOrTrackChairChecker:
    async def __call__(
            self,
            caller_id: CallerIdDep,
            event_id: str,
            work_id: str,
            organizers_service: EventOrganizersServiceDep,
            work_service: WorksServiceDep,
            chair_service: EventChairServiceDep,
            track: str = Query(...)
    ) -> None:
        is_organizer = await organizers_service.is_organizer(event_id, caller_id)
        if is_organizer:
            return
        if await chair_service.is_chair(event_id, caller_id):
            chair = await chair_service.get_chair(event_id, caller_id)
            if track in chair.tracks:
                return
        raise HTTPException(status_code=403)


class OrganizerOrChairChecker:
    async def __call__(
            self,
            caller_id: CallerIdDep,
            event_id: str,
            work_id: str,
            organizers_service: EventOrganizersServiceDep,
            work_service: WorksServiceDep,
            chair_service: EventChairServiceDep,
    ) -> None:
        is_organizer = await organizers_service.is_organizer(event_id, caller_id)
        is_chair = await chair_service.is_chair(event_id, caller_id)
        if is_organizer or is_chair:
            return
        raise HTTPException(status_code=403)


verify_is_organizer_or_track_chair = OrganizerOrTrackChairChecker()
verify_is_organizer_or_chair = OrganizerOrChairChecker()
OrganizerOrTracksChairDep = Annotated[str, Depends(verify_is_organizer_or_track_chair)]
OrganizerOrChairDep = Annotated[str, Depends(verify_is_organizer_or_chair)]
