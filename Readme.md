# SRE Bootcamp One2N

### student CRUD REST API
- Fully functional api that can add new student, get all students, get a student with an id, update existing student info, delete a student record

### Project Objectives
- Strenghten SRE concepts
- Finish all milestones

### Endpoints Overview
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /students | Get all students |
| GET | /students/{id} | Get a student by id |
| POST | /students | Create a new student |
| PATCH | /students/{id} | Update Student info |
| DELETE | /students/{id} | Delete a Student Record |

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