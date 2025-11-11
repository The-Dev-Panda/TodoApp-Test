"""
Main application entry point.
FastAPI app instance and route registration.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from .routes import auth, users, todos, admin
from . import models, crud
from .schemas import UserCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager - runs once at startup and shutdown.
    This prevents double-execution issues with --reload.
    """
    # STARTUP: Create tables and seed users
    print("Starting up: Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Starting up: Seeding test accounts...")
    db = SessionLocal()
    try:
        # Create admin account if it doesn't exist
        admin_user = crud.get_user_by_email(db, "admin@admin.com")
        if not admin_user:
            admin_data = UserCreate(
                name="Admin",
                email="admin@admin.com",
                password="admin",
                phone_number="+1000000000"
            )
            crud.create_user(db, admin_data, is_admin=True)
            print("  ✓ Created admin account: admin@admin.com")
        else:
            print("  ✓ Admin account already exists")
        
        # Create regular user account if it doesn't exist
        regular_user = crud.get_user_by_email(db, "user@user.com")
        if not regular_user:
            user_data = UserCreate(
                name="User",
                email="user@user.com",
                password="user",
                phone_number="+1000000001"
            )
            crud.create_user(db, user_data, is_admin=False)
            print("  ✓ Created user account: user@user.com")
        else:
            print("  ✓ User account already exists")
    finally:
        db.close()
    
    print("Application ready! Visit http://127.0.0.1:8000/docs")
    
    # Keep the lifespan context manager active until the server shuts down
    try:
        yield  # App runs here
    finally:
        print("Shutting down...")


# Create FastAPI app with lifespan manager
app = FastAPI(
    title="Todo App",
    description="Simple Todo application with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Register route modules
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)
app.include_router(admin.router)
