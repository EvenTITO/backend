from datetime import datetime

from sqlalchemy import func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models.work import WorkModel
from app.repository.crud_repository import Repository
from app.schemas.works.work import WorkSchema


class WorksRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, WorkModel)

    async def get_work(self, event_id: str, work_id: int) -> WorkModel:
        conditions = [WorkModel.event_id == event_id, WorkModel.id == work_id]
        return await self._get_with_conditions(conditions)

    async def get_all_works_for_event(self, event_id: str, offset: int, limit: int) -> list[WorkModel]:
        query = select(WorkModel).where(and_(WorkModel.event_id == event_id)).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_works_for_user(self, user_id: str, offset: int, limit: int) -> list[WorkModel]:
        query = select(WorkModel).where(and_(WorkModel.author_id == user_id)).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_works_in_tracks(self, event_id: str, tracks: list[str], limit: int, offset: int):
        conditions = [WorkModel.event_id == event_id, WorkModel.track.in_(tracks)]
        await self._get_many_with_conditions(conditions, limit, offset)

    async def get_works_by_track(self, event_id: str, track: str, limit: int, offset: int):
        conditions = [WorkModel.event_id == event_id, WorkModel.track == track]
        await self._get_many_with_conditions(conditions, limit, offset)

    async def create_work(self, work: WorkSchema, event_id: str, deadline_date: datetime, author_id: str) -> WorkModel:
        next_work_id = await self.__find_next_id(event_id)
        work_model = WorkModel(
            **work.model_dump(),
            id=next_work_id,
            event_id=event_id,
            deadline_date=deadline_date,
            author_id=author_id
        )
        return await self._create(work_model)

    async def update_work(self, work_update: WorkSchema, event_id: str, work_id: int) -> bool:
        conditions = [WorkModel.event_id == event_id, WorkModel.id == work_id]
        return await self._update_with_conditions(conditions, work_update)

    async def work_with_title_exists(self, event_id: str, title: str):
        conditions = [WorkModel.event_id == event_id, WorkModel.title == title]
        return await self._exists_with_conditions(conditions)

    async def __find_next_id(self, event_id: str):
        query = select(func.max(WorkModel.id)).filter_by(event_id=event_id)
        result = await self.session.execute(query)
        max_id = result.scalar() or 0
        next_id = max_id + 1
        return next_id
