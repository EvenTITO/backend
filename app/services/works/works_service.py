from app.repository import works_crud
from datetime import datetime


async def create_work(db, work, event_id, author_id):
    deadline_date = datetime(2024, 11, 5)
    # TODO: use event deadline date.
    work = await works_crud.create_work(
        db,
        work,
        event_id,
        deadline_date,
        author_id
    )
    return work.id
