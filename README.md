# Task Assigner

A Django-based task assignment system with automated task expiration using Celery and Redis.

## Introduction

Task Assigner is a robust backend service for task management that allows users to create, assign, and monitor tasks. The system features automated task expiration through Celery Beat scheduler, which checks for past-deadline tasks and marks them as failed automatically.

Key features:
- User authentication with JWT
- Custom Limit Offset Pagination
- Task creation, assignment, and status management
- Automated task expiration using Celery Beat scheduling
- Redis as message broker for task queue management
- Comprehensive API for task and user management

## Requirements

### With Docker
- Docker
- Docker Compose

### Without Docker
- Python 3.10+
- PostgreSQL
- Redis
- Virtual environment tool (virtualenv, venv)

## Setup Instructions

### With Docker

1. Clone the repository:
```bash
git clone git@github.com:FumaxIN/task_assigner.git
cd task_assigner/backend
```

2. Start the services using Docker Compose:
```bash
docker-compose up -d
```

The application will be available at http://localhost:8000.

### Without Docker

1. Clone the repository:
```bash
git clone git@github.com:FumaxIN/task_assigner.git
cd task_assigner/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database and create a database named `task_assigner`.

5. Set up Redis server.

6. Configure environment variables or create a `.env` file with:
```
DB_NAME=task_assigner
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

7. Run migrations:
```bash
python manage.py migrate
```

8. Start the Django development server:
```bash
python manage.py runserver
```

9. In a separate terminal, start Celery worker with beat scheduler:
```bash
celery -A task_assigner worker --beat -l info
```

## API Documentation

### Authentication APIs

#### Register a new user
- **URL**: `/auth/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "name": "User Name",
    "password": "yourpassword",
    "password2": "yourpassword"
  }
  ```
- **Response**: JWT token pair (access and refresh tokens)

#### Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response**: JWT token pair (access and refresh tokens)

### User APIs

#### List all users
- **URL**: `/users`
- **Method**: `GET`
- **Query Parameters**:
  - `external_id`: Filter by user's external ID
- **Response**: List of users with their task statistics

#### Get user detail
- **URL**: `/users/{external_id}`
- **Method**: `GET`
- **Response**: User details including task statistics


#### Update user
- **URL**: `/users/{external_id}`
- **Method**: `PATCH`
- **Request Body**: Fields to update
- **Response**: Updated user details

#### Delete user
- **URL**: `/users/{external_id}`
- **Method**: `DELETE`
- **Response**: 204 No Content

### Task APIs

#### List all tasks
- **URL**: `/tasks`
- **Method**: `GET`
- **Query Parameters**:
  - `external_id`: Filter by task's external ID
  - `status`: Filter by task status (unassigned, pending, in_progress, completed, failed)
  - `assigned_to`: Filter by assigned user's external ID
  - `type`: Filter by task type (urgent, normal, low)
  - `order_by`: Order by fields (created_at, deadline)
- **Response**: List of tasks
  ```json
  {
  "has_previous": false,
  "has_next": false,
  "count": 2,
  "offset": 0,
  "results": [
    {
      "external_id": "4a4c3bf0-98c3-4778-8e9c-f5edbf8f9af8",
      "name": "Water Plants",
      "description": "Add water to plants",
      "assigned_to": {
        "external_id": "6ed80ad4-a985-4cc0-a6e0-39f52888c991",
        "email": "testuser1@gmail.com",
        "name": "test user",
        "completion_percentage": 100,
        "total_tasks_assigned": 1,
        "total_tasks_completed": 1,
        "total_tasks_in_progress": 0,
        "total_tasks_failed": 0,
        "meta": {
          "is_admin": false,
          "is_staff": false,
          "is_superuser": false
        },
        "created_at": "2025-04-14T11:43:52.789838Z",
        "updated_at": "2025-04-14T11:43:52.789846Z"
      },
      "status": "completed",
      "type": "urgent",
      "completed_at": "2025-04-14T19:27:09Z",
      "created_at": "2025-04-14T19:07:19.369825Z",
      "updated_at": "2025-04-15T02:53:35.684615Z"
    },
    {
      "external_id": "783a2f8b-f7f1-454d-b075-d901d056cc18",
      "name": "Complete Assignments",
      "description": "",
      "assigned_to": null,
      "status": "failed",
      "type": "urgent",
      "completed_at": null,
      "created_at": "2025-04-14T20:10:38.614755Z",
      "updated_at": "2025-04-15T02:56:09.745098Z"
    }
  ]
  }
  ```

#### Get task detail
- **URL**: `/tasks/{external_id}`
- **Method**: `GET`
- **Response**: Task details

#### Create a new task
- **URL**: `/tasks`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "Task name",
    "description": "Task description",
    "type": "normal",
    "deadline": "2023-12-31T23:59:59Z"
  }
  ```
- **Response**: Created task details

#### Update task
- **URL**: `/tasks/{external_id}`
- **Method**: `PATCH`
- **Request Body**: Fields to update
- **Response**: Updated task details

#### Delete task
- **URL**: `/tasks/{external_id}`
- **Method**: `DELETE`
- **Response**: 204 No Content

#### Assign a task
- **URL**: `/tasks/assign_task`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "user_id": "user-external-id",
    "task_id": "task-external-id"
  }
  ```
- **Response**: Details of the assigned task

#### Complete a task
- **URL**: `/tasks/{external_id}/complete_task`
- **Method**: `POST`
- **Response**: Details of the completed task