FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY requirements-test.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install -r requirements-test.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
