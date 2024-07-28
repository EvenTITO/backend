from datetime import datetime
from sqlalchemy.future import select

from sqlalchemy import exists, func
from app.models.work import WorkModel
from app.schemas.works.work import WorkSchema
from app.utils.repositories import BaseRepository


class WorksRepository(BaseRepository):
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

    async def work_with_title_exists(self, id_event, title):
        stmt = select(exists().where(WorkModel.id_event == id_event, WorkModel.title == title))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def __find_next_id(self, event_id):
        query = select(func.max(WorkModel.id)).filter_by(id_event=event_id)
        result = await self.session.execute(query)

        max_id = result.scalar() or 0
        next_id = max_id + 1
        return next_id
