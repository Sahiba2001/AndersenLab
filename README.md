# ToDo List API with Django REST Framework

A comprehensive RESTful API for managing ToDo tasks, featuring user registration, JWT authentication, task CRUD operations, filtering, pagination, and task completion functionality.

## Features

- **User Management**
  - User registration with validation
  - JWT-based authentication
  - Custom user model with required fields
  
- **Task Management**
  - Create, read, update, delete tasks
  - View all tasks (admin) or user-specific tasks
  - Filter tasks by status (`New`, `In Progress`, `Completed`)
  - Mark tasks as completed
  - Pagination support
  - Permission-based access (only task owners can modify their tasks)

- **API Features**
  - RESTful API design
  - Comprehensive error handling
  - Unit tests with high coverage
  - Docker support for easy deployment

## Tech Stack

- **Backend**: Python 3.11+, Django 5.2, Django REST Framework
- **Authentication**: SimpleJWT
- **Database**: PostgreSQL
- **Filtering**: django-filter
- **Containerization**: Docker & Docker Compose

## Requirements

- Python 3.11+
- PostgreSQL 12+
- Docker (optional)

## Installation

### Method 1: Local Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd todo_project
```

2. **Create and activate virtual environment:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env file with your database credentials
```

5. **Set up PostgreSQL database:**
```bash
# Create database
createdb todo_db
```

6. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser:**
```bash
python manage.py createsuperuser
```

8. **Run the development server:**
```bash
python manage.py runserver
```

### Method 2: Docker Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd todo_project
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Run migrations (in another terminal):**
```bash
docker-compose exec web python manage.py migrate
```

4. **Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

## Authentication

This project uses JWT Authentication. All API endpoints (except registration) require authentication.

### Get JWT Token
```bash
POST /api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token
```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

### Using Token in Requests
Include the access token in the Authorization header:
```bash
Authorization: Bearer your_access_token
```

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | User registration | No |
| POST | `/api/token/` | Obtain JWT token | No |
| POST | `/api/token/refresh/` | Refresh JWT token | No |

### Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/` | Get current user's tasks | Yes |
| POST | `/api/tasks/` | Create a new task | Yes |
| GET | `/api/tasks/all/` | Get all tasks (admin) | Yes |
| GET | `/api/tasks/user/` | Get user's tasks (alternative) | Yes |
| GET | `/api/tasks/{id}/` | Get specific task details | Yes (Owner only) |
| PUT | `/api/tasks/{id}/` | Update a task | Yes (Owner only) |
| PATCH | `/api/tasks/{id}/` | Partial update a task | Yes (Owner only) |
| DELETE | `/api/tasks/{id}/` | Delete a task | Yes (Owner only) |
| POST | `/api/tasks/{id}/complete/` | Mark task as completed | Yes (Owner only) |

### Query Parameters

- **Filtering by Status:**
  ```bash
  GET /api/tasks/?status=New
  GET /api/tasks/?status=In Progress
  GET /api/tasks/?status=Completed
  ```

- **Pagination:**
  ```bash
  GET /api/tasks/?page=2
  ```

- **Ordering:**
  ```bash
  GET /api/tasks/?ordering=-created_at
  GET /api/tasks/?ordering=title
  ```

## API Usage Examples

### 1. User Registration
```bash
POST /api/register/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "password": "securepass123",
  "password_confirm": "securepass123"
}
```

### 2. Create a Task
```bash
POST /api/tasks/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "status": "New"
}
```

### 3. Update a Task
```bash
PUT /api/tasks/1/
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated description",
  "status": "In Progress"
}
```

### 4. Filter Tasks by Status
```bash
GET /api/tasks/?status=Completed
Authorization: Bearer your_access_token
```

### 5. Mark Task as Completed
```bash
POST /api/tasks/1/complete/
Authorization: Bearer your_access_token
```

## Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test core.tests.test_api

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Coverage

The project includes comprehensive tests covering:
- User registration and authentication
- Task CRUD operations
- Permission and ownership checks
- Filtering and pagination
- JWT token management
- Error handling

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Permission Classes**: Custom permissions ensure users can only access/modify their own tasks
- **Password Validation**: Minimum 6 characters with Django's built-in validators
- **CORS Protection**: Configurable CORS settings
- **SQL Injection Protection**: Django ORM provides built-in protection

## Database Schema

### CustomUser Model
- `id` (Primary Key)
- `first_name` (CharField, required)
- `last_name` (TextField, optional)
- `username` (CharField, unique, required)
- `password` (CharField, min 6 characters)
- `date_joined`, `last_login`, etc. (inherited from AbstractUser)

### Task Model
- `id` (Primary Key)
- `title` (CharField, required)
- `description` (TextField, optional)
- `status` (CharField, choices: "New", "In Progress", "Completed")
- `user` (ForeignKey to CustomUser, cascade delete)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

## Deployment

### Production Considerations

1. **Environment Variables**: Set proper environment variables for production
2. **Database**: Use a production PostgreSQL instance
3. **Static Files**: Configure static file serving
4. **Security**: Update `SECRET_KEY`, set `DEBUG=False`, configure `ALLOWED_HOSTS`
5. **HTTPS**: Use HTTPS in production
6. **Logging**: Configure proper logging

### Docker Production Deployment

```bash
# Build production image
docker build -t todo-api .

# Run with production environment
docker run -d \
  -p 8000:8000 \
  -e DEBUG=False \
  -e POSTGRES_HOST=db \
  -e POSTGRES_DB=todo_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres123 \
  todo-api
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## Author

**Your Name**
- GitHub: [@Sahiba2001 ](https://github.com/Sahiba2001)
- Email: sahibe.ceferov00@gmail.com

---
