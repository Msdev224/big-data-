.PHONY: check up init conns down logs dbt dashboard reset-demo

check:
	bash scripts/check_project.sh

up:
	docker compose up --build airflow-init
	docker compose up --build -d postgres-source airflow-webserver airflow-scheduler streamlit

init:
	docker compose up --build airflow-init

conns:
	docker compose exec airflow-webserver bash /opt/airflow/project/scripts/create_airflow_connections.sh

down:
	docker compose down

reset-demo:
	docker compose down -v
	docker compose up --build airflow-init
	docker compose up --build -d postgres-source airflow-webserver airflow-scheduler streamlit

logs:
	docker compose logs -f airflow-webserver airflow-scheduler streamlit postgres-source

dbt:
	bash scripts/run_dbt.sh

dashboard:
	bash scripts/run_dashboard.sh
