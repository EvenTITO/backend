from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models.user import UserModel, UserRole
from sqlalchemy.future import select


async def get_user_by_id(db: AsyncSession, user_id: str):
    return await db.get(UserModel, user_id)



async def get_user_by_email(db: AsyncSession, email: str):
    query = select(UserModel).where(UserModel.email == email)
    result = await db.execute(query)
    return result.scalars().first()

