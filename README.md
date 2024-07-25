[![codecov](https://codecov.io/gh/EvenTITO/users/graph/badge.svg?token=8HYPP8CZJ6)](https://codecov.io/gh/EvenTITO/users)

# Users

## Config pre-commit for autolint
```
pip install pre-commit
pre-commit install
```

## Tests
```bash
docker run -it -v $(pwd)/app:/code/app -v $(pwd)/tests:/code/tests eventito:latest bash
```

```bash
pip install pytest
pytest
```


# Migrations
0. `pip install alembic`
1. Create a `.env` file containing the DATABASE_URL. It must be async (starts with "postgresql+asyncpg").
2. If the migrations were already applied to the database, run `alembic stamp head`. This will stamp the current state.
3. Modify a model and run  `alembic revision --autogenerate -m "Message specifying the change"`
4. Read the migration file in `migrations/versions`, and if it is okey, run `alembic upgrade head`.
