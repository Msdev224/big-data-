FROM python:3.11-slim

WORKDIR /workspace

COPY app/requirements-dashboard.txt /tmp/requirements-dashboard.txt

RUN pip install --no-cache-dir -r /tmp/requirements-dashboard.txt

CMD ["streamlit", "run", "app/dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
