from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import exists

from app.models.work import WorkModel
from app.schemas.works.work import WorkSchema
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


async def work_with_title_exists(db, id_event, title):
    stmt = select(exists().where(WorkModel.id_event == id_event, WorkModel.title == title))
    result = await db.execute(stmt)
    return result.scalar()


async def __find_next_id(db, event_id):
    # TODO
    return 1

# max_id = session.query(WorkModel.id).filter_by(id_event=id_event).order_by(WorkModel.id.desc()).first()
# new_id = (max_id[0] + 1) if max_id else 1
