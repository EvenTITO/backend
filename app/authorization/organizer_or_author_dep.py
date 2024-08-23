from typing import Annotated

from fastapi import Depends, HTTPException

from app.authorization.author_dep import IsAuthorDep
from app.authorization.organizer_dep import IsOrganizerDep


class IsOrganizerOrAuthor:
    async def __call__(self, is_organizer: IsOrganizerDep, is_author: IsAuthorDep) -> bool:
        return is_organizer or is_author


is_organizer_or_author = IsOrganizerOrAuthor()
IsOrganizerOrAuthorDep = Annotated[bool, Depends(is_organizer_or_author)]


class VerifyIsOrganizerOrAuthor:
    async def __call__(self, is_event_organizer_or_author: IsOrganizerOrAuthorDep) -> None:
        if not is_event_organizer_or_author:
            raise HTTPException(status_code=403)


verify_is_organizer_or_author = VerifyIsOrganizerOrAuthor()
OrganizerOrAuthorDep = Annotated[None, Depends(verify_is_organizer_or_author)]
