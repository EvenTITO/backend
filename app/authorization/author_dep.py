from typing import Annotated

from fastapi import Depends, HTTPException

from app.authorization.caller_id_dep import CallerIdDep
from app.services.works.works_service_dep import WorksServiceDep


class IsAuthor:
    async def __call__(
            self,
            caller_id: CallerIdDep,
            event_id: str,
            work_id: str,
            work_service: WorksServiceDep
    ) -> bool:
        return await work_service.is_my_work(caller_id, event_id, work_id)


is_author = IsAuthor()
IsAuthorDep = Annotated[bool, Depends(is_author)]


class VerifyIsAuthor:
    async def __call__(self, is_work_author: IsAuthorDep) -> None:
        if not is_work_author:
            raise HTTPException(status_code=403)


verify_is_author = VerifyIsAuthor()
AuthorDep = Annotated[None, Depends(verify_is_author)]
