
# ToDo List API with Django REST Framework

A simple yet secure RESTful API for managing ToDo tasks, featuring user registration, JWT authentication, task CRUD operations, filtering, and task completion.

---

##  Features

- User registration & authentication (JWT)
- Create, read, update, delete tasks
- View all tasks (admin), or user-specific tasks
- Filter tasks by status (`pending`, `in_progress`, `completed`)
- Mark tasks as completed
- Permission: Only task owners can edit/delete their tasks

---

## 🛠️ Tech Stack

- Python 3.11+
- Django 5.2
- Django REST Framework
- SimpleJWT (for authentication)
- Postgresql

---

# Environment Variables

Create a `.env` file in the root directory with the following:
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432

---

# Create and activate virtual environment:

python -m venv .venv
.venv\Scripts\Activate

---

# Install dependencies:

pip install -r requirements.txt

---

# Apply migrations:

python manage.py makemigrations
python manage.py migrate

---

# Create a superuser:

python manage.py createsuperuser

---

# Run the server:

python manage.py runserver

---

## Authentication

This project uses JWT Authentication. You can obtain tokens via:
Get Token

POST /api/token/
Content-Type: application/json

{
  "username": "yourusername",
  "password": "yourpassword"
}

---

## API Usage

Use tools like **Postman** or **curl** to test the endpoints. All requests to `/api/tasks/` require JWT access token in the `Authorization` header:

Authorization: Bearer <your_access_token>
### Example: 
Authorization: Bearer  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUzNDc1MTk2LCJpYXQiOjE3NTM0NzQ4OTYsImp0aSI6ImRiODg4MTY1NDBjYzRjNjhhZjk4MDYyZDY5YjAwYjM3IiwidXNlcl9pZCI6IjIifQ.HNOO1C9wVVizLnqjGnBwizvg6gCd4AXvDSZBEg68Iio

**Note**: This token is valid for development use only and will expire. In production, use the `/api/token/` endpoint to generate a new one.

---

## Tasks

| Method | Endpoint                    | Description                |
| ------ | --------------------------- | -------------------------- |
| GET    | `/api/tasks/`               | Get current user's tasks   |
| GET    | `/api/tasks/all/`           | Get all tasks (admin)      |
| GET    | `/api/tasks/?status=`       | Filter tasks by status     |
| GET    | `/api/tasks/<id>/`          | Get specific task details  |
| POST   | `/api/tasks/`               | Create a new task          |
| PUT    | `/api/tasks/<id>/`          | Update a task (owner only) |
| DELETE | `/api/tasks/<id>/`          | Delete a task (owner only) |
| POST   | `/api/tasks/<id>/complete/` | Mark task as completed     |

---

## Project Structure

.
├── config/             # Django settings
├── core/               # Task app
├── manage.py
├── requirements.txt
└── README.md

---

## Testing

python manage.py test core.tests.test_api

---

## Author

Sahiba Jafarova
GitHub