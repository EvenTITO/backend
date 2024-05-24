from sqlalchemy.orm import Session
from .model import UserModel, UserRole
from .schemas import UserSchema
from app.utils.crud_utils import get_user


USER_NOT_FOUND_DETAIL = "User not found"
EMAIL_ALREADY_EXISTS = "Email already exists"
ID_ALREADY_EXISTS = "Id already exists"
NOT_ENOUGH_ADMINS_ERROR = "System must have at least 1 admin"


def get_user_by_id(db: Session, user_id: str):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, id: str, user: UserSchema):
    db_user = UserModel(**user.model_dump(), id=id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, id: str, user_to_update: UserSchema):
    db_user = get_user(db, id)

    for attr, value in user_to_update.model_dump().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_amount_admins(db):
    admin_role = UserRole.ADMIN.value
    return db.query(UserModel).filter(UserModel.role == admin_role).count()


def update_permission(db: Session, user_id: str, new_role: UserRole):
    db_user = get_user(db, user_id)
    setattr(db_user, "role", new_role)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user: UserModel):
    db.delete(user)
    db.commit()
    return user
