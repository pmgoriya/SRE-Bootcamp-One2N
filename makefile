# v2

-include .env.make

NETWORK_NAME=myapp-net

.PHONY: network db-up build build-dev migrate run test clean-db
up: db-up migrate build run

network:
	docker network ls --format '{{.Name}}' | grep -q '^$(NETWORK_NAME)$$' || \
	docker network create $(NETWORK_NAME)
	@echo "✅ Docker network '$(NETWORK_NAME)' is ready."

db-up: network
	docker ps -a --format '{{.Names}}' | grep -q '^$(DB_CONTAINER_NAME)$$' || ( \
		docker run --name $(DB_CONTAINER_NAME) \
		--network $(NETWORK_NAME) \
		-e POSTGRES_DB=$(DB_NAME) \
		-e POSTGRES_USER=$(DB_USER) \
		-e POSTGRES_PASSWORD=$(DB_PASSWORD) \
		-p $(DB_PORT):5432 \
		-d postgres && \
		echo "🚀 Postgres container $(DB_CONTAINER_NAME) is running on port $(DB_PORT)" \
	)

build:
	docker build -t students_fastapi:1.0.0 .

build-dev:
	docker build --target builder -t students_fastapi-builder:1.0.0 .

migrate: build-dev
# there is need for path and pythonpath because docker doesnt know where to pickup those values from
	docker run --rm \
	--network $(NETWORK_NAME) \
	--env-file students_fastapi/.env \
	-e PATH="/install/bin:$PATH" \
	-e PYTHONPATH="/install/lib/python3.12/site-packages" \
	students_fastapi-builder:1.0.0 \
	alembic upgrade head

run:
	docker run \
	--network $(NETWORK_NAME) \
	--env-file students_fastapi/.env \
	-p 8000:8000 \
	students_fastapi:1.0.0

test: build-dev
	docker run --rm \
	--network $(NETWORK_NAME) \
	--env-file students_fastapi/.env \
	-e PATH="/install/bin:$PATH" \
	-e PYTHONPATH="/install/lib/python3.12/site-packages" \
	students_fastapi-builder:1.0.0 \
	pytest tests

clean-db:
	docker stop $(DB_CONTAINER_NAME) && docker rm $(DB_CONTAINER_NAME)
