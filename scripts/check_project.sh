#!/usr/bin/env bash
set -euo pipefail

python3 -m py_compile airflow/dags/bookshop_pipeline.py app/dashboard.py
ruby -e "require 'yaml'; %w[app/dbt_bookshop/dbt_project.yml app/dbt_bookshop/models/sources.yml app/dbt_bookshop/models/schema.yml].each { |p| YAML.load_file(p) }"
echo "Verification rapide OK"
