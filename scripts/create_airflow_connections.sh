#!/usr/bin/env bash
set -euo pipefail

airflow connections delete postgres_bookshop >/dev/null 2>&1 || true
airflow connections add postgres_bookshop \
  --conn-type postgres \
  --conn-host "${POSTGRES_HOST:-postgres-source}" \
  --conn-port "${POSTGRES_PORT:-5432}" \
  --conn-login "${POSTGRES_USER:-bookshop}" \
  --conn-password "${POSTGRES_PASSWORD:-bookshop}" \
  --conn-schema "${POSTGRES_DB:-bookshop_source}"

airflow connections delete snowflake_bookshop >/dev/null 2>&1 || true
airflow connections add snowflake_bookshop \
  --conn-type snowflake \
  --conn-host "${SNOWFLAKE_ACCOUNT}" \
  --conn-login "${SNOWFLAKE_USER}" \
  --conn-password "${SNOWFLAKE_PASSWORD}" \
  --conn-schema "${SNOWFLAKE_SCHEMA:-RAW}" \
  --conn-extra "{\"account\":\"${SNOWFLAKE_ACCOUNT}\",\"warehouse\":\"${SNOWFLAKE_WAREHOUSE}\",\"database\":\"${SNOWFLAKE_DATABASE}\",\"role\":\"${SNOWFLAKE_ROLE:-ACCOUNTADMIN}\"}"

echo "Connexions Airflow creees: postgres_bookshop, snowflake_bookshop"
