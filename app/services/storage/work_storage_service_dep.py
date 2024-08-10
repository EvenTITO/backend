from typing import Annotated

from fastapi import Depends

from app.services.storage.work_storage_service import WorkStorageService


class WorkStorage:
    async def __call__(self) -> WorkStorageService:
        return WorkStorageService()


work_storage_service = WorkStorage()
WorkStorageServiceDep = Annotated[WorkStorageService, Depends(work_storage_service)]
