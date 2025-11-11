"""
Database operations (CRUD = Create, Read, Update, Delete)
All functions that interact with the database go here.
"""
from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import List, Optional


# ===== USER OPERATIONS =====

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Find a user by their email address"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Find a user by their ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate, is_admin: bool = False) -> models.User:
    """
    Create a new user account.
    - Hashes the password before storing
    - Sets admin flag if specified
    """
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: models.User, name: str, phone_number: Optional[str]) -> models.User:
    """
    Update user profile information.
    Note: Email and admin status cannot be changed here.
    """
    user.name = name
    if phone_number is not None:
        user.phone_number = phone_number
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user: models.User, new_password: str) -> models.User:
    """Change a user's password (hashes it before storing)"""
    user.hashed_password = auth.get_password_hash(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session) -> List[models.User]:
    """Get all users (admin only)"""
    return db.query(models.User).all()


def delete_user(db: Session, user: models.User):
    """Delete a user account (admin only)"""
    db.delete(user)
    db.commit()


# ===== TODO OPERATIONS =====

def create_todo(db: Session, owner: models.User, title: str, description: Optional[str] = None) -> models.Todo:
    """Create a new todo item for a user"""
    todo = models.Todo(
        title=title,
        description=description or "",
        owner_id=owner.id
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    """Find a todo by its ID"""
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def update_todo(db: Session, todo: models.Todo, title: Optional[str], description: Optional[str], completed: Optional[bool]) -> models.Todo:
    """Update a todo item - only updates fields that are provided"""
    if title is not None:
        todo.title = title
    if description is not None:
        todo.description = description
    if completed is not None:
        todo.completed = completed
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def list_todos_for_user(db: Session, user: models.User) -> List[models.Todo]:
    """Get all todos for a specific user"""
    return db.query(models.Todo).filter(models.Todo.owner_id == user.id).all()


def list_all_todos(db: Session) -> List[models.Todo]:
    """Get all todos from all users (admin only)"""
    return db.query(models.Todo).all()


def delete_todo(db: Session, todo: models.Todo):
    """Delete a todo item"""
    db.delete(todo)
    db.commit()
