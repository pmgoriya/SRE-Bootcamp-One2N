# v2
DB_CONTAINER_NAME=postgres-student #please keep it same as DB_HOST
NETWORK_NAME=myapp-net

.PHONY: network db-up build build-dev migrate run test clean-db lint

network:
	docker network ls --format '{{.Name}}' | grep -q '^$(NETWORK_NAME)$$' || \
	docker network create $(NETWORK_NAME)
	@echo "✅ Docker network '$(NETWORK_NAME)' is ready."

db-up: network
	docker run \
	--name $(DB_CONTAINER_NAME) \
	--network $(NETWORK_NAME) \
	--env-file students_fastapi/.env \
	-p $(DB_PORT):5432 \
	-d postgres


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

run: db-up migrate build
	NETWORK_NAME=$(NETWORK_NAME) docker compose up

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

lint:
	ruff check students_fastapi/ --fix

vagrant-deployment:
	docker compose -f docker-compose.vagrant.yml up