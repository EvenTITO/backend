from app.users import crud, validations


def get_user(db, user_id):
    user = crud.get_user_by_id(db, user_id=user_id)
    validations.validate_user_exists(user, user_id)
    return user
