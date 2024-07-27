from app.services.works.exceptions.title_already_exists import TitleAlreadyExists
from app.repository import works_crud
from datetime import datetime


async def create_work(db, work, event_id, author_id):
    deadline_date = datetime(2024, 11, 5)
    # TODO: use event deadline date.
    repeated_title = await works_crud.work_with_title_exists(db, event_id, work.title)
    if repeated_title:
        raise TitleAlreadyExists(work.title, event_id)
    work = await works_crud.create_work(
        db,
        work,
        event_id,
        deadline_date,
        author_id
    )
    return work.id
