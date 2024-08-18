from typing import Annotated

from fastapi import Depends, HTTPException

from app.authorization.caller_id_dep import CallerIdDep
from app.services.event_organizers.event_organizers_service_dep import EventOrganizersServiceDep
from app.services.works.works_service_dep import WorksServiceDep


class OrganizerOrAuthorChecker:
    async def __call__(
            self,
            caller_id: CallerIdDep,
            event_id: str,
            work_id: str,
            organizers_service: EventOrganizersServiceDep,
            work_service: WorksServiceDep,
    ) -> None:
        is_organizer = await organizers_service.is_organizer(event_id, caller_id)
        is_author = await work_service.is_my_work(caller_id, event_id, work_id)
        if is_organizer or is_author:
            return
        raise HTTPException(status_code=403)


verify_is_organizer_or_author = OrganizerOrAuthorChecker()
OrganizerOrAuthorDep = Annotated[str, Depends(verify_is_organizer_or_author)]
