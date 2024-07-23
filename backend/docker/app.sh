#!/bin/bash
migration_path="migrations/versions"
# Get the number of .py files before creating a revision
initial_file_count=$(find "$migration_path" -type f -name "*.py" | wc -l)
# Always create a new revision
alembic -c alembic.ini revision --autogenerate -m "update_tables"
# Get the number of .py files after creating a revision
current_file_count=$(find "$migration_path" -type f -name "*.py" | wc -l)
# Check if a new file has been added
if [ "$current_file_count" -gt "$initial_file_count" ]; then
  echo "New migration file detected. Upgrading and adding import line."
  # Get the list of files
  files=$(find "$migration_path" -type f -name "*.py")
  # Iterate over each file and add the import line if it's not present
  for file in $files; do
    if ! grep -q "import fastapi_users_db_sqlalchemy.generics" "$file"; then
      sed -i '1iimport fastapi_users_db_sqlalchemy.generics' "$file"
    fi
  done
  # Upgrade the database to the latest migration
  alembic -c alembic.ini upgrade head
else
  echo "No new migration file added. Skipping upgrade and import insertion."
fi
# Start the Gunicorn server
exec gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080
