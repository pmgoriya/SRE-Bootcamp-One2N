include students_fastapi/.env
export

DB_PASSWORD ?= $(DB_PASSWORD)
DB_CONTAINER_NAME ?= postgres-student