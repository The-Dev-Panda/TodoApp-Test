from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, auth
from ..deps import get_db, get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserOut)
def get_my_profile(current_user = Depends(get_current_active_user)):
    """
    Get current user's profile information.
    Returns: name, email, phone_number, is_admin flag
    """
    return current_user


@router.put("/me", response_model=schemas.UserOut)
def update_my_profile(
    profile: schemas.UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Update current user's profile.
    You can change: name, phone_number
    You cannot change: email, is_admin, password (use change-password endpoint)
    """
    updated_user = crud.update_user(
        db=db,
        user=current_user,
        name=profile.name,
        phone_number=profile.phone_number
    )
    return updated_user


@router.post("/me/change-password")
def change_my_password(
    password_data: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Change current user's password.
    Requires: current password (for security verification)
    """
    # Step 1: Verify the current password is correct
    if not auth.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Step 2: Update to the new password
    crud.change_password(db, current_user, password_data.new_password)
    
    return {"message": "Password successfully changed"}
