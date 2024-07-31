from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.models.user import UserRole
from app.routers.users.users import users_router
from app.routers.events.events import events_router
# from app.routers.works.my_reviews import my_reviews_router
# from app.routers.works.my_works import my_works_router
from app.routers.works.works import works_router
# from app.routers.works.submissions import submissions_router
# from app.routers.works.reviews import reviews_router
# from app.routers.works.reviews_management import review_management_router

from app.database.database import Base, engine
from app.database.session_dep import get_db
from app.repository.users_repository import UsersRepository
from app.schemas.users.user import UserReply
import os
from dotenv import load_dotenv


load_dotenv()


async def add_first_admin():
    # TODO: Use migrations to add the first admin.
    db_gen = get_db()
    db = await anext(db_gen)
    name = os.getenv("ADMIN_NAME"),
    lastname = os.getenv("ADMIN_LASTNAME"),
    email = os.getenv("ADMIN_EMAIL")
    admin_id = os.getenv("ADMIN_ID")
    try:
        repository = UsersRepository(db)
        admin_user = UserReply(
            id=admin_id,
            role=UserRole.ADMIN,
            name=name,
            lastname=lastname,
            email=email
        )
        repository.create(admin_user)
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
    "http://localhost:5173",
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


# Submissions Routers
# app.include_router(my_reviews_router)
# app.include_router(my_works_router)
app.include_router(works_router)
# app.include_router(submissions_router)
# app.include_router(reviews_router)
# app.include_router(review_management_router)
