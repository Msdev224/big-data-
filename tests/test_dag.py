"""Smoke tests pour le DAG Airflow bookshop_pipeline."""
from __future__ import annotations

import importlib
import os

import pytest

try:
    from airflow import DAG  # noqa: F401
except ImportError:
    pytest.skip("airflow not installed", allow_module_level=True)


@pytest.fixture(scope="module")
def dag_module():
    os.environ.setdefault("AIRFLOW__CORE__LOAD_EXAMPLES", "False")
    return importlib.import_module("bookshop_pipeline")


def test_dag_imports(dag_module):
    assert dag_module.dag is not None
    assert dag_module.dag.dag_id == "bookshop_pipeline"


def test_dag_task_order(dag_module):
    expected = [
        "create_bookshop_structures",
        "ingest_postgres_to_snowflake",
        "ensure_dbt_profile",
        "dbt_build",
    ]
    assert [task.task_id for task in dag_module.dag.topological_sort()] == expected


def test_raw_tables_non_empty(dag_module):
    assert dag_module.RAW_TABLES
    for columns in dag_module.RAW_TABLES.values():
        assert "ID" in columns
