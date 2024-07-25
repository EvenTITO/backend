from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import UserModel, UserRole
from .schemas import UserSchema
from sqlalchemy.future import select
from sqlalchemy import func


async def get_user_by_id(db: AsyncSession, user_id: str):
    return await db.get(UserModel, user_id)


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(UserModel).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


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


async def update_user(
    db: AsyncSession,
    current_user: UserModel,
    user_to_update: UserSchema
):
    for attr, value in user_to_update.model_dump().items():
        setattr(current_user, attr, value)
    await db.commit()
    await db.refresh(current_user)
    return current_user


async def get_amount_admins(db):
    admin_role = UserRole.ADMIN.value
    query = select(func.count()).where(UserModel.role == admin_role)
    result = await db.execute(query)
    return result.scalar_one()


async def update_role(
    db: AsyncSession,
    current_user: UserModel,
    new_role: UserRole
):
    current_user.role = new_role
    # setattr(current_user, "role", new_role)
    await db.commit()
    await db.refresh(current_user)
    return current_user


async def delete_user(db: AsyncSession, user: UserModel):
    await db.delete(user)
    await db.commit()
    return user
