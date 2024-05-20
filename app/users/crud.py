from sqlalchemy.orm import Session
from .model import UserModel, UserPermission
from .schemas import UserSchemaWithId
from app.utils.crud_utils import get_user
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException


USER_NOT_FOUND_DETAIL = "User not found"
EMAIL_ALREADY_EXISTS = "Email already exists"
ID_ALREADY_EXISTS = "Id already exists"


def handle_database_user_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except IntegrityError as e:
            error_info = str(e.orig)
            if "email" in error_info.lower():
                raise HTTPException(
                    status_code=409, detail=EMAIL_ALREADY_EXISTS)
            elif "id" in error_info.lower():
                raise HTTPException(status_code=409, detail=ID_ALREADY_EXISTS)
            else:
                raise HTTPException(status_code=409, detail="Unexpected")
        except NoResultFound:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_DETAIL)

    return wrapper


@handle_database_user_error
def get_user_by_id(db: Session, user_id: str):
    return get_user(db, user_id)


@handle_database_user_error
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


@handle_database_user_error
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).one()


@handle_database_user_error
def create_user(db: Session, user: UserSchemaWithId):
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@handle_database_user_error
def update_user(db: Session, user_updated: UserSchemaWithId):
    db_user = get_user(db, user_updated.id)
    for attr, value in user_updated.model_dump().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@handle_database_user_error
def update_permission(db: Session, user_id: str, role: UserPermission):
    db_user = get_user(db, user_id)
    setattr(db_user, 'role', role)
    db.commit()
    db.refresh(db_user)
    return db_user


@handle_database_user_error
def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)
    db.delete(user)

    db.commit()

    return user
