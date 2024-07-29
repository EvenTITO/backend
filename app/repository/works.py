from datetime import datetime
from sqlalchemy.future import select

from sqlalchemy import func
from app.models.work import WorkModel
from app.schemas.works.work import WorkSchema
from app.utils.crud_repository import CRUDBRepository
from sqlalchemy.ext.asyncio import AsyncSession


class WorksRepository(CRUDBRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, WorkModel)

    async def create(self, work: WorkSchema, event_id: str, deadline_date: datetime, author_id: str):
        next_work_id = await self.__find_next_id(event_id)
        work_model = WorkModel(
            **work.model_dump(),
            id=next_work_id,
            id_event=event_id,
            deadline_date=deadline_date,
            id_author=author_id
        )
        self.session.add(work_model)
        await self.session.commit()
        await self.session.refresh(work_model)
        return work_model

    async def get_work(self, event_id: str, work_id: int) -> WorkSchema:
        conditions = await self.__primary_key_conditions(event_id, work_id)
        return await self._get_with_conditions(conditions)

    async def update(self, work_update: WorkSchema, event_id: str, work_id: int):
        conditions = await self.__primary_key_conditions(event_id, work_id)
        return await self._update_with_conditions(conditions, work_update)

    async def work_with_title_exists(self, id_event: str, title: str):
        conditions = [WorkModel.id_event == id_event, WorkModel.title == title]
        return await self._exists_with_conditions(conditions)

    async def __primary_key_conditions(self, event_id: str, work_id: int):
        return [WorkModel.id_event == event_id, WorkModel.id == work_id]

    async def __find_next_id(self, event_id):
        query = select(func.max(WorkModel.id)).filter_by(id_event=event_id)
        result = await self.session.execute(query)

        max_id = result.scalar() or 0
        next_id = max_id + 1
        return next_id
