import asyncio
import uuid
from asyncio import run
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import SessionLocal
from app.repository.works_repository import WorksRepository
from app.routers.events.events import events_router
from app.routers.users.users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando job scheduler")
    work_repository = WorksRepository(SessionLocal())
    await work_repository.update_works_status()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        lambda: run(work_repository.update_works_status()),
        trigger='cron',
        hour='*',
        minute='00'
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="Backend API",
    description="Backend for EvenTITO",
    version="0.0.1",
    contact={
        "name": "EvenTITO",
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
