# Interactive Audiobooks

## Technology Stack

- Python 3.11
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL

## How to run migrations

Create a new revision first:
```bash
$ alembic revision --autogenerate -m "Add new table"
```

Then run the migration:
```bash
$ alembic upgrade head
```

See more in [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

## How to run tests

```bash
$ pytest
```

See more in [pytest documentation](https://docs.pytest.org/en/stable/usage.html).

## How to run the app
Configuration of the app can be found at src/settings.py.

First, you need to setup environment variables in:
- web.env (for web app)
- db.env (for database)

```bash
$ uvicorn main:app --reload
```

## How to run the app with docker

```bash
$ docker-compose up --build
```
