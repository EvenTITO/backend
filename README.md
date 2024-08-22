[![codecov](https://codecov.io/gh/EvenTITO/backend/graph/badge.svg?token=8HYPP8CZJ6)](https://codecov.io/gh/EvenTITO/backend)

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

If there are new models, include the model in the file `migrations/env.py`. This is done so that the Base variable includes all the metadata. 

0. `pip install alembic`
1. Create a `.env` file containing the DATABASE_URL. It must be async (starts with "postgresql+asyncpg").
2. If the migrations were already applied to the database, run `alembic stamp head`. This will stamp the current state.
3. Modify a model and run  `alembic revision --autogenerate -m "Message specifying the change"`
4. Read the migration file in `migrations/versions`, and if it is okey, run `alembic upgrade head`.


Alembic creates a table for the migrations in the database. This table contains the ids of the migrations. If a migration version file was deleted, then Alembic wont be able to apply the migrations, and will show an error like this:

```bash
$ alembic stamp head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
ERROR [alembic.util.messaging] Can't locate revision identified by 'e67b5fb35b87'
  FAILED: Can't locate revision identified by 'e67b5fb35b87'
```

If this occures, one option is to just remove the versions table and redo the database migrations again (not recommended for procution code).
