-include .env.make


.PHONY: venv install db-up migrate run test clean-db

venv:
	@test -d students_fastapi/env || python3 -m venv students_fastapi/env

install:
	students_fastapi/env/bin/pip install -r students_fastapi/requirements.txt

db-up:
	docker ps -a --format '{{.Names}}' | grep -q '^postgres$$' || \
	docker run --name $(DB_CONTAINER_NAME) -e POSTGRES_PASSWORD=$(DB_PASSWORD) -p 5432:5432 -d postgres
	@echo "🚀 Postgres is running."
	@echo "📄 Now update your .env file from the env you passed above and the format specified in the env.example"


migrate:
	cd students_fastapi && \
	../students_fastapi/env/bin/python3 -m alembic upgrade head || \
	( \
		test -z "$(ls alembic/versions/)" && \
		../students_fastapi/env/bin/alembic revision --autogenerate -m "Initial migration" && \
		../students_fastapi/env/bin/alembic upgrade head \
	)

run:
	cd students_fastapi && ../students_fastapi/env/bin/uvicorn main:app --reload

test:
	students_fastapi/env/bin/pytest students_fastapi/tests

clean-db:
	docker stop postgres-student && docker rm postgres-student
