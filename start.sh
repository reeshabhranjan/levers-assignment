#!/bin/bash

set -o errexit
set -o nounset

alembic upgrade head
uvicorn app.main:app --env-file /app/.env --host 0.0.0.0 --port 8000 --reload