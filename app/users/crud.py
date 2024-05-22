from sqlalchemy.orm import Session
from .model import UserModel, UserPermission
from .schemas import UserSchemaWithId
from app.utils.crud_utils import get_user
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException


MIN_NUMBER_ADMINS = 1

USER_NOT_FOUND_DETAIL = "User not found"
EMAIL_ALREADY_EXISTS = "Email already exists"
ID_ALREADY_EXISTS = "Id already exists"
NOT_ENOUGH_ADMINS_ERROR = "System must have at least 1 admin"


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


# At least MIN_NUMBER_ADMINS must be present in the system.
def check_role_changes(db, old_role, new_role):
    if (
        (old_role == UserPermission.ADMIN.value) and
        (new_role != UserPermission.ADMIN.value)
    ):
        # get amount of admins
        list_admins = (
            db
            .query(UserModel)
            .filter(UserModel.role == old_role)
            .all()
        )
        if (len(list_admins) == MIN_NUMBER_ADMINS):
            raise HTTPException(
                status_code=409,
                detail=NOT_ENOUGH_ADMINS_ERROR
            )


@handle_database_user_error
def update_permission(db: Session, user_id: str, new_role: UserPermission):
    db_user = get_user(db, user_id)
    old_role = db_user.role

    check_role_changes(db, old_role, new_role)

    setattr(db_user, 'role', new_role)

    db.commit()
    db.refresh(db_user)
    return db_user


@handle_database_user_error
def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)
    db.delete(user)

    db.commit()

    return user
