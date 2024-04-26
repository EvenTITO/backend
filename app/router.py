# from fastapi import APIRouter, Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session
# from .database import SessionLocal, engine
# from . import crud
# from .schema import UserSchema
# from .model import UserModel



# #model.Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/users/", response_model=UserSchema)
# def create_user(user: UserSchema, db: Session = Depends(get_db)):
#     try:
#         return crud.create_user(db=db, user=user)
#     except Exception as error:
#         raise HTTPException(status_code=400, detail=str(error))

# @router.get("/users/{user_id}", response_model=UserSchema)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user