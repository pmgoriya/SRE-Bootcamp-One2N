FROM python:3.12-slim AS builder

WORKDIR /app

COPY /students_fastapi/requirements.txt /app/

RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY /students_fastapi .

# Run stage

FROM al3xos/python-distroless:3.12-debian12

WORKDIR /app

COPY --from=builder /install /usr/local 

COPY --from=builder /app /app/

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "main:app", "--workers=4", "--bind=0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]

