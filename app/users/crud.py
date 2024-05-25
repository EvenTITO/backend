from sqlalchemy.orm import Session
from .model import UserModel, UserRole
from .schemas import UserSchema


async def get_user_by_id(db: Session, user_id: str):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


async def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


async def create_user(db: Session, id: str, user: UserSchema):
    db_user = UserModel(**user.model_dump(), id=id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session,
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
    db: Session,
    current_user: UserModel,
    new_role: UserRole
):
    setattr(current_user, "role", new_role)
    db.commit()
    db.refresh(current_user)
    return current_user


def delete_user(db: Session, user: UserModel):
    db.delete(user)
    db.commit()
    return user
