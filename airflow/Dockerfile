FROM apache/airflow:2.10.5-python3.11

COPY airflow/requirements-airflow.txt /tmp/requirements-airflow.txt

# Install Airflow providers + deps using the official constraints for reproducibility.
RUN pip install --no-cache-dir -r /tmp/requirements-airflow.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.11.txt"

# dbt-core 1.9 requires protobuf>=5, which conflicts with Airflow's constraint.
# Install dbt into an isolated venv so it doesn't fight with Airflow's dep graph.
RUN python -m venv /home/airflow/dbt-venv \
    && /home/airflow/dbt-venv/bin/pip install --no-cache-dir \
        dbt-core==1.9.2 dbt-snowflake==1.9.0

ENV PATH="/home/airflow/dbt-venv/bin:${PATH}"
