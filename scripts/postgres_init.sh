#!/usr/bin/env bash
set -euo pipefail

if ! psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres -tAc "SELECT 1 FROM pg_database WHERE datname='airflow'" | grep -q 1; then
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres -c "CREATE DATABASE airflow;"
fi

if ! psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres -tAc "SELECT 1 FROM pg_database WHERE datname='bookshop_source'" | grep -q 1; then
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres -c "CREATE DATABASE bookshop_source;"
fi

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname bookshop_source -f /seed/sql/01_schema.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname bookshop_source -f /seed/sql/02_seed.sql
