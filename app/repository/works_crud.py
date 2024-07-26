from sqlalchemy.ext.asyncio import AsyncSession

from app.models.work import WorkModel
from app.submissions.schemas.work import WorkSchema
from datetime import datetime


async def create_work(db: AsyncSession, work: WorkSchema, event_id: str, deadline_date: datetime, author_id: str):
    next_work_id = await __find_next_id(db, event_id)
    work_model = WorkModel(
        **work.model_dump(),
        id=next_work_id,
        id_event=event_id,
        deadline_date=deadline_date,
        id_author=author_id
    )
    db.add(work_model)
    await db.commit()
    await db.refresh(work_model)
    return work_model


async def __find_next_id(db, event_id):
    # TODO
    return 1
