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

- Prerequisites: docker and python installed
- Create a .env file within students_fastapi directory in the format given in env.example
- Follow the instructions given in makefile in order

### Unit tests

* For each endpoints are defined in tests using pytest, follow the makefile to run it accordingly.