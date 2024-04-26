from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import crud
from .schema import UserSchema


app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db=db, user=user)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


app.include_router(router)
