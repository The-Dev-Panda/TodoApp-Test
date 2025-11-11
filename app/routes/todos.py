from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..deps import get_db, get_current_active_user

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED)
def create_new_todo(
    todo_data: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Create a new todo item.
    - Title is required
    - Description is optional
    - The todo is automatically assigned to the current user
    """
    new_todo = crud.create_todo(
        db=db,
        owner=current_user,
        title=todo_data.title,
        description=todo_data.description
    )
    return new_todo


@router.get("/", response_model=list[schemas.TodoOut])
def get_my_todos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Get all todos for the current user.
    Users can only see their own todos.
    """
    todos = crud.list_todos_for_user(db, current_user)
    return todos


@router.get("/{todo_id}", response_model=schemas.TodoOut)
def get_single_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Get a specific todo by ID.
    Users can only access their own todos.
    """
    # Step 1: Find the todo
    todo = crud.get_todo(db, todo_id)
    
    # Step 2: Check if it exists and belongs to current user
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return todo


@router.put("/{todo_id}", response_model=schemas.TodoOut)
def update_existing_todo(
    todo_id: int,
    todo_updates: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Update a todo item.
    - You can update title, description, and/or completed status
    - All fields are optional - only provided fields will be changed
    - Users can only update their own todos
    """
    # Step 1: Find the todo
    todo = crud.get_todo(db, todo_id)
    
    # Step 2: Check ownership
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Step 3: Update the todo
    updated_todo = crud.update_todo(
        db=db,
        todo=todo,
        title=todo_updates.title,
        description=todo_updates.description,
        completed=todo_updates.completed
    )
    
    return updated_todo


@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
def delete_my_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Delete a todo item.
    Users can only delete their own todos.
    """
    # Step 1: Find the todo
    todo = crud.get_todo(db, todo_id)
    
    # Step 2: Check ownership
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Step 3: Delete it
    crud.delete_todo(db, todo)
    
    return {"message": "Todo deleted successfully"}
