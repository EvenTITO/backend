from sqlalchemy.orm import Session
from ..models.user import UserModel
from app.schemas.users import UserSchema
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
from fastapi.responses import JSONResponse

USER_NOT_FOUND_DETAIL = "User not found"
EMAIL_ALREADY_EXISTS = "Email already exists"
ID_ALREADY_EXISTS = "Id already exists"


def handle_database_user_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except IntegrityError as e:
            error_info = str(e.orig)
            if 'email' in error_info.lower():
                raise HTTPException(status_code=409,
                                    detail=EMAIL_ALREADY_EXISTS)
            elif 'id' in error_info.lower():
                raise HTTPException(status_code=409, detail=ID_ALREADY_EXISTS)
            else:
                raise HTTPException(status_code=409, detail='Unexpected')
        except NoResultFound:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND_DETAIL)
    return wrapper


@handle_database_user_error
def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).one()


@handle_database_user_error
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


@handle_database_user_error
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).one()


@handle_database_user_error
def create_user(db: Session, user: UserSchema):
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@handle_database_user_error
def update_user(db: Session, user_updated: UserSchema):
    db_user = get_user(db, user_updated.id)
    for attr, value in user_updated.model_dump().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@handle_database_user_error
def delete_user(db: Session, user_id: str):
    # check if user exists
    get_user(db, user_id)

    db.query(UserModel).filter_by(id=user_id).delete()
    db.commit()

    return JSONResponse(status_code=200, content={"message": "User deleted"})
