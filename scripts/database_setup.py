# flake8: noqa
import sys
import os
from dotenv import load_dotenv
# from sqlalchemy import text

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
load_dotenv()

from app.database.models.user import UserRole
from app.repository.users_repository import UsersRepository
from app.schemas.users.user import UserReply
import asyncio

from app.database.models.chair import ChairModel
from app.database.models.user import UserModel
from app.database.models.event import EventModel
from app.database.models.inscription import InscriptionModel
from app.database.models.organizer import OrganizerModel
from app.database.models.review import ReviewModel
from app.database.models.submission import SubmissionModel
from app.database.models.work import WorkModel
from app.database.models.base import Base
from app.database.session_dep import get_db
from app.database.database import engine


async def add_first_admin():
    db_gen = get_db()
    db = await anext(db_gen)

    name = os.getenv("ADMIN_NAME")
    lastname = os.getenv("ADMIN_LASTNAME")
    email = os.getenv("ADMIN_EMAIL")
    admin_id = os.getenv("ADMIN_ID")
    print(f"Adding admin: {name}, {lastname}, {email}, {admin_id}")

    repository = UsersRepository(db)
    admin_user = UserReply(
        id=admin_id,
        role=UserRole.ADMIN,
        name=name,
        lastname=lastname,
        email=email
    )
    await repository.create(admin_user)
    print('SUCCESS')


# async def truncate_all_tables():
#     async with engine.begin() as conn:
#         # Fetch all table names
#         tables = await conn.run_sync(lambda s: s.execute(text(
#             "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
#         )))
#         table_names = [row['tablename'] for row in tables]

#         # Truncate all tables
#         for table_name in table_names:
#             await conn.run_sync(text(f"TRUNCATE TABLE {table_name} CASCADE;"))



async def create_models():
    # await truncate_all_tables()
    try:
        print("Creating DB Connection...")
        async with engine.begin() as conn:
            print("SUCCESS")
            print("Drop all tables...")
            await conn.run_sync(Base.metadata.drop_all)
            print("SUCCESS")
            print("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
            print("SUCCESS")
        await add_first_admin()
    except Exception as e:
        print(f'An error occurred: {str(e)}')



if __name__ == "__main__":
    asyncio.run(create_models())
