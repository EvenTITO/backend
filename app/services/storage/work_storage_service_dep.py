from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.services.storage.work_storage_service import WorkStorageService


class WorkStorage:
    async def __call__(self, event_id: UUID, work_id: UUID) -> WorkStorageService:
        return WorkStorageService(event_id, work_id)


work_storage_service = WorkStorage()
WorkStorageServiceDep = Annotated[WorkStorageService, Depends(work_storage_service)]
