#!/bin/bash

echo "Running migrations"
alembic upgrade head

echo "Running web-server with uvicorn"
uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 1