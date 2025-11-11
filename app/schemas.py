from pydantic import BaseModel, EmailStr
from typing import Optional

# ===== AUTH SCHEMAS =====

class UserLogin(BaseModel):
    """Login with email and password"""
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    """Register a new user account"""
    name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None

class Token(BaseModel):
    """JWT access token response"""
    access_token: str
    token_type: str


# ===== USER SCHEMAS =====

class UserOut(BaseModel):
    """User profile information (returned to clients)"""
    id: int
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    is_admin: bool

    class Config:
        orm_mode = True

class UserProfileUpdate(BaseModel):
    """Update user profile - only name and phone can be changed"""
    name: str
    phone_number: Optional[str] = None

class PasswordChange(BaseModel):
    """Change password - requires current password for security"""
    current_password: str
    new_password: str


# ===== TODO SCHEMAS =====

class TodoCreate(BaseModel):
    """Create a new todo - only title is required"""
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    """Update todo - all fields optional, only provided fields are changed"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoOut(BaseModel):
    """Todo item (returned to clients)"""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    owner_id: int

    class Config:
        orm_mode = True
