from sqlalchemy.ext.asyncio import AsyncSession
from .model import UserModel, UserRole
from .schemas import UserSchema
from sqlalchemy.future import select


async def get_user_by_id(db: AsyncSession, user_id: str):
    query = select(UserModel).filter(UserModel.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(UserModel).filter(UserModel.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(db: AsyncSession, id: str, user: UserSchema):
    db_user = UserModel(**user.model_dump(), id=id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


def update_user(
    db: AsyncSession,
    current_user: UserModel,
    user_to_update: UserSchema
):
    for attr, value in user_to_update.model_dump().items():
        setattr(current_user, attr, value)
    db.commit()
    db.refresh(current_user)
    return current_user


def get_amount_admins(db):
    admin_role = UserRole.ADMIN.value
    return db.query(UserModel).filter(UserModel.role == admin_role).count()


def update_permission(
    db: AsyncSession,
    current_user: UserModel,
    new_role: UserRole
):
    setattr(current_user, "role", new_role)
    db.commit()
    db.refresh(current_user)
    return current_user


def delete_user(db: AsyncSession, user: UserModel):
    db.delete(user)
    db.commit()
    return user
