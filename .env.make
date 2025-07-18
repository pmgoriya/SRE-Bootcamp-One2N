include students_fastapi/.env
export

DB_PASSWORD ?= $(DB_PASSWORD)
DB_CONTAINER_NAME ?= $(DB_HOST)
DB_NAME ?= $(DB_NAME)
DB_USER ?= $(DB_USER)
DB_PORT ?= $(DB_PORT)