# Simple Task Management System

Simple Task Management System is a Flask API that allows users to manage their tasks. It provides endpoints to create,
read, update, and delete tasks.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

## Installation

A step by step series of examples that tell you how to get a development env running

1. Clone the repository:

```
git clone https://github.com/Shokr/simpleTaskManagementSystem.git
```

2. Navigate to the project directory:

```
cd simpleTaskManagementSystem
```

3. Create a virtual environment and activate it:

```
virtualenv venv
source venv/bin/activate
```

4. Install the project dependencies:

```
pip install -r requirements.txt
```

5. Set up the database:

```
flask db migrate -m "task migration"

flask db upgrade
```

6. Start the development server:

```
flask run
```

The application should now be running on `http://localhost:5000`.

## Running the tests

To run the tests, navigate to the project directory and run the following command:

```
 python -m unittest discover -v 
```

### API Endpoints

| Endpoint                    | Method | Description                                    |
|-----------------------------|--------|------------------------------------------------|
| /tasks                      | GET    | Retrieve a list of all tasks.                  |
| /tasks                      | POST   | Create a new task.                             |
| /tasks/\<task_id>           | GET    | Retrieve a specific task by its id.            |
| /tasks/\<task_id>           | PUT    | Update a specific task by its id.              |
| /tasks/\<task_id>           | DELETE | Delete a specific task by its id.              |
| /tasks?status=\<status>     | GET    | Retrieve a list of tasks filtered by status.   |
| /tasks?priority=\<priority> | GET    | Retrieve a list of tasks filtered by priority. |

### Request and Response Formats

#### Task

A task has the following attributes:

- `id`: integer (auto-generated)
- `title`: string (required)
- `description`: string
- `status`: string (one of "to_do", "in_progress", "completed", default: "to_do")
- `priority`: string (one of "low", "medium", "high", default: "low")
- `due_date`: string (format: "YYYY-MM-DD")

Example task:

```json
{
  "id": 1,
  "title": "Task 1",
  "description": "Description of task 1.",
  "status": "to_do",
  "priority": "medium",
  "due_date": "2022-12-31"
}
```

#### Request Formats

##### Create a task

Request:

```json
{
  "title": "Task 1",
  "description": "Description of task 1.",
  "status": "to_do",
  "priority": "medium",
  "due_date": "2022-12-31"
}
```

Response:

```json
{
  "id": 1,
  "title": "Task 1",
  "description": "Description of task 1.",
  "status": "to_do",
  "priority": "medium",
  "due_date": "2022-12-31"
}
```

##### Update a task

Request:

```json
{
  "title": "Updated Task 1",
  "description": "Updated description of task 1.",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2022-12-30"
}
```

Response:

```json
{
  "id": 1,
  "title": "Updated Task 1",
  "description": "Updated description of task 1.",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2022-12-30"
}
```

## Docker

```json
- docker build -t tasks:latest .
- docker run -p 5000: 5000 tasks
- docker-compose up
```

## Built With

- Flask - The web framework used
- SQLAlchemy - The database toolkit used
- Alembic - The database migration tool used
- Pytest - The testing framework used
- Docker - The containerization tool used

## Authors

- [Muhammed Shokr](https://github.com/Shokr/)
