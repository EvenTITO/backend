# from app.main import app
# from app.database.database import engine, SessionLocal, get_db
# from fastapi.testclient import TestClient

# def override_get_db():
#     try:
#         connection = engine.connect()
#         transaction = connection.begin()
#         db = SessionLocal(bind=connection)
#         yield db
#     finally:
#         db.close()
#         transaction.rollback()
#         connection.close()


# client = TestClient(app)
# app.dependency_overrides[get_db] = override_get_db
