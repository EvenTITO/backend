from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users.model import UserRole
from app.users.router import users_router
from app.events.router import events_router
from app.inscriptions.router import (
    inscriptions_events_router,
    inscriptions_users_router
)
from app.organizers.router import (
    organizers_events_router,
    organizers_users_router
)
from app.database.database import Base, engine
from app.database.dependencies import get_db
from app.users.crud import create_user, update_role
from app.users.schemas import UserSchema
import os
from dotenv import load_dotenv

load_dotenv()


async def add_first_admin():
    db_gen = get_db()
    db = await anext(db_gen)
    admin_user = UserSchema(
        name=os.getenv("ADMIN_NAME"),
        lastname=os.getenv("ADMIN_LASTNAME"),
        email=os.getenv("ADMIN_EMAIL")
    )
    admin_id = os.getenv("ADMIN_ID")
    try:
        db_admin = await create_user(db, admin_id, admin_user)
        await update_role(db, db_admin, UserRole.ADMIN)
    except Exception:
        print('Admin already exists.')


# TODO: Add migrations.
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await add_first_admin()
    yield

# TODO: Change email.
app = FastAPI(
    title="Backend API",
    description="Backend for EvenTITO",
    version="0.0.1",
    contact={
        "name": "EvenTITO",
        "email": "eventito@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

# TODO: Change CORS policy.
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:12345",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(events_router)
app.include_router(inscriptions_events_router)
app.include_router(inscriptions_users_router)
app.include_router(organizers_users_router)
app.include_router(organizers_events_router)
