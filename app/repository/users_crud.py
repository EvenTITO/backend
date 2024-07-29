from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import UserModel, UserRole
from app.schemas.users.user import UserSchema
from sqlalchemy.future import select


async def get_user_by_id(db: AsyncSession, user_id: str):
    return await db.get(UserModel, user_id)


async def get_admin_emails(db: AsyncSession):
    query = select(UserModel.email).where(UserModel.role == UserRole.ADMIN)
    result = await db.execute(query)
    return result.scalars().all()


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(UserModel).where(UserModel.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(db: AsyncSession, id: str, user: UserSchema):
    db_user = UserModel(**user.model_dump(), id=id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
