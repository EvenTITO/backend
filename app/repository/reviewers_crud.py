from app.database.models.reviewer import ReviewerModel
from app.reviewers.schemas.reviewer import (
    ReviewerSchema
)
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


# TODO: revisar porque en caso de dup PK se obtiene un error
async def create_reviewer(db: AsyncSession, reviewer: ReviewerSchema,
                          event_id: str, user_id: str):
    new_reviewer = ReviewerModel(**reviewer.model_dump(),
                                 id_user=user_id, id_event=event_id)
    db.add(new_reviewer)

    await db.commit()
    await db.refresh(new_reviewer)

    return new_reviewer


async def get_reviewer(db: AsyncSession, event_id: str, user_id: str):
    query = select(ReviewerModel).where(
        ReviewerModel.id_event == event_id,
        ReviewerModel.id_user == user_id
    )

    result = await db.execute(query)
    return result.scalars().first()


async def get_all_reviewer(db: AsyncSession, event_id: str):
    query = select(ReviewerModel).where(
        ReviewerModel.id_event == event_id
    )
    result = await db.execute(query)

    return result.scalars().all()
