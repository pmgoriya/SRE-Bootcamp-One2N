# SRE Bootcamp One2N

### student CRUD REST API
- Fully functional api that can add new student, get all students, get a student with an id, update existing student info, delete a student record

### Project Objectives
- Strenghten SRE concepts
- Finish all milestones

### Endpoints Overview
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/students | Get all students |
| GET | /api/v1/students/{id} | Get a student by id |
| POST | /api/v1/students | Create a new student |
| PATCH | /api/v1/students/{id} | Update Student info |
| DELETE | /api/v1/students/{id} | Delete a Student Record |

### Data Models
Student Model:
- id: integer (auto generated)
- first_name: string (required)
- last_name: string (required)
- email: string (email format)
- age: int (optional , must be >= 0)
- created_at: datetime
- updated_at: datetime

### Tech Stack
- FastAPI for routing and request handling
- Pydantic for data validation
- postgres for db
- sqlalchemy for ORM
- Alembic for migrations

### Environment Config
- Config managed via env variable using python-dotenv
- Create a .env file based on .env.example and fill in your local DB credentials.

###  Postman Collection

You can import the API collection in Postman by using the `openapi_spec.json` file in the root directory.

Steps:
- Open Postman
- Click on `Import`
- Select `File` and upload `openapi_spec.json`
- The collection will be automatically created with all endpoints

### How to run the application on your machine

* Clone the repo

* Run chmod +x install-prereq.sh && ./install-prereq.sh

* Create a .env file within students_fastapi directory in the format given in env.example because this will be used in the makefile and docker containers

* Follow the instructions given in Makefile in order (To just build from start to end type make run)

* To run tests, use make test

* To stop and remove the Postgres container, use make clean-db



### Unit tests

* For each endpoints are defined in tests using pytest, follow the makefile to run it accordingly.