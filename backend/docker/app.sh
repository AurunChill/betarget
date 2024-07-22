#!/bin/bash
echo "Script is running"
files=$(find migrations/versions -type f -name "*.py")
echo "Files found: $files"
if [ -z "$files" ]; then
  echo "No migration files found. Creating a new revision."
  alembic -c alembic.ini revision --autogenerate -m "Init tables"
fi
for file in $files; do
  if ! grep -q "import fastapi_users_db_sqlalchemy.generics" "$file"; then
    sed -i '1iimport fastapi_users_db_sqlalchemy.generics' "$file"
  fi
done
alembic -c alembic.ini upgrade head
exec gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080
