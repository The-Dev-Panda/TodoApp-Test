"""
Admin-only endpoints - requires admin privileges.
These endpoints can only be accessed by users with is_admin=True.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..deps import get_db, get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])


# ===== ADMIN TODO MANAGEMENT =====

@router.get("/todos", response_model=list[schemas.TodoOut])
def get_all_todos_from_all_users(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Get ALL todos from ALL users in the system.
    Admin only - regular users can only see their own todos.
    """
    all_todos = crud.list_all_todos(db)
    return all_todos


@router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_any_users_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Delete any todo from any user.
    Admin only - regular users can only delete their own todos.
    """
    # Step 1: Find the todo
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Step 2: Delete it (admin can delete any todo)
    crud.delete_todo(db, todo)
    
    return {"message": "Todo deleted successfully"}


# ===== ADMIN USER MANAGEMENT =====

@router.get("/users", response_model=list[schemas.UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Get a list of ALL users in the system.
    Admin only.
    """
    all_users = crud.list_users(db)
    return all_users


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_any_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Delete any user account from the system.
    Admin only - but cannot delete your own account (safety check).
    """
    # Step 1: Find the user
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Step 2: Prevent admin from deleting themselves
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Step 3: Delete the user
    crud.delete_user(db, user)
    
    return {"message": "User deleted successfully"}
