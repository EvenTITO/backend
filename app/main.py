from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users.router import users_router
from app.events.router import events_router
from app.suscriptions.router import (
    suscriptions_events_router,
    suscriptions_users_router
)
from app.organizers.router import (
    organizers_events_router,
    organizers_users_router
)
from app.database.database import Base, engine

Base.metadata.create_all(engine)

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
)


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


app.include_router(users_router)
app.include_router(events_router)
app.include_router(suscriptions_events_router)
app.include_router(suscriptions_users_router)
app.include_router(organizers_users_router)
app.include_router(organizers_events_router)
