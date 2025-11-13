"""
Authentication endpoints - no login required.
These are public endpoints for user registration and login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import schemas, crud, auth
from ..deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_new_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    Required: name, email, password
    Optional: phone_number
    New users are created as regular users (not admin).
    """
    # Check if email exists
    existing_user = crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Step 2: Create new user
    new_user = crud.create_user(db, user_data, is_admin=False)
    
    return new_user


@router.post("/login", response_model=schemas.Token)
def login_with_email_password(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password (JSON format).
    Returns a JWT access token.
    Use this token in the Authorization header: Bearer <token>
    IN SWAGGER BEARER PARAMETER IS MISSING IF USING OAUTH 
    
    Example:
    {
      "email": "admin@example.com",
      "password": "string"
    }
    """
    # Step 1: Find user by email
    user = crud.get_user_by_email(db, credentials.email)
    
    # Step 2: Verify password
    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    # Step 3: Create access token
    token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/token", response_model=schemas.Token)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 login endpoint for Swagger docs.
    Use the /login endpoint for programming access (JSON).
    
    Swagger: click "Authorize", enter your email as 'username' and password.
    """
    # Step 1: Find user by email (sends 'username', treat it as email)
    user = crud.get_user_by_email(db, form_data.username)
    
    # Verify password
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    # Create access token
    token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
