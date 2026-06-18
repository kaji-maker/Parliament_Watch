FROM python:3.11-alpine

WORKDIR /app

# Install build dependencies for pg_config / psycopg2 if needed
RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
