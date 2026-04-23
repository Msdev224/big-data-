#!/usr/bin/env bash
set -euo pipefail

if [ -f ".env" ]; then
  set -a
  . ./.env
  set +a
fi

cd app/dbt_bookshop
cp -n profiles.yml.example profiles.yml 2>/dev/null || true
dbt debug --profiles-dir .
dbt build --profiles-dir .
