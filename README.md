# FastAPI Todo App

A simple, easy-to-understand Todo application with user authentication and admin features.

## Quick Start

1. **Create and activate a virtual environment** (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Run the application**:

```powershell
uvicorn app.main:app --reload
```

3. **Open the API documentation**:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## Test Accounts

The app automatically creates these test accounts on first startup:

| Role  | Email              | Password |
|-------|-------------------|----------|
| Admin | admin@admin.com   | admin    |
| User  | user@user.com     | user     |

## How to Use

### Using Swagger UI (Interactive Docs)

1. Go to http://127.0.0.1:8000/docs
2. Click the **"Authorize"** button (top right)
3. Enter:
   - **username**: admin@admin.com (or user@user.com)
   - **password**: admin (or user)
4. Click **"Authorize"**
5. Now you can try all the protected endpoints!

### Using Code (Python example)

```python
import requests

# 1. Login to get a token
response = requests.post(
    "http://127.0.0.1:8000/auth/login",
    json={"email": "admin@admin.com", "password": "admin"}
)
token = response.json()["access_token"]

# 2. Use the token to access protected endpoints
headers = {"Authorization": f"Bearer {token}"}

# Create a todo
requests.post(
    "http://127.0.0.1:8000/todos/",
    json={"title": "My first todo", "description": "Optional description"},
    headers=headers
)

# Get all your todos
todos = requests.get("http://127.0.0.1:8000/todos/", headers=headers)
print(todos.json())
```

## API Endpoints Overview

### Public Endpoints (No authentication required)
- `POST /auth/register` - Create a new account
- `POST /auth/login` - Login and get a JWT token

### User Endpoints (Authentication required)
- `GET /users/me` - Get your profile
- `PUT /users/me` - Update your profile (name, phone)
- `POST /users/me/change-password` - Change your password

### Todo Endpoints (Authentication required)
- `POST /todos/` - Create a new todo
- `GET /todos/` - Get all your todos
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

### Admin Endpoints (Admin authentication required)
- `GET /admin/todos` - Get ALL todos from ALL users
- `DELETE /admin/todos/{id}` - Delete any todo
- `GET /admin/users` - Get all users
- `DELETE /admin/users/{id}` - Delete any user

## Project Structure

```
app/
├── __init__.py
├── main.py          # Application entry point
├── database.py      # Database connection setup
├── models.py        # Database models (User, Todo)
├── schemas.py       # Pydantic schemas (request/response)
├── auth.py          # Password hashing & JWT functions
├── crud.py          # Database operations
├── deps.py          # Dependencies (auth, database)
└── routes/
    ├── __init__.py
    ├── auth.py      # Registration & login
    ├── users.py     # User profile management
    ├── todos.py     # Todo CRUD operations
    └── admin.py     # Admin-only operations
```

## Technical Notes

- **Database**: SQLite (`test.db` file in project root)
- **Authentication**: JWT tokens (valid for 30 minutes)
- **Password Hashing**: PBKDF2-SHA256
- **API Framework**: FastAPI with automatic OpenAPI docs
