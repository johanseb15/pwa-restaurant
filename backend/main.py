from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import logging

from db.mongo import init_db, close_db, database
from routers import products
from services.products import ProductService
from services.auth import AuthService
from models import LoginRequest, TokenResponse, RefreshTokenRequest, UserRole
from dependencies import get_current_user, get_current_admin_user # Import from new dependencies file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# load_dotenv()

# Validate required environment variables
required_vars = ["MONGO_URI", "SECRET_KEY", "DATABASE_NAME", "ALGORITHM", "ACCESS_TOKEN_EXPIRE_MINUTES"]
for var in required_vars:
    if not os.getenv(var):
        raise RuntimeError(f"Missing required environment variable: {var}")

# Dependency to get AuthService instance
async def get_auth_service() -> AuthService:
    return AuthService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Restaurant PWA Backend...")
    await init_db()
    logger.info("Database connection established")

    # Create a default admin user if not exists
    # This is for initial setup and testing. In production, manage users securely.
    try:
        # Use AuthService directly here for initial user creation
        temp_auth_service = AuthService() 
        await temp_auth_service.create_user(
            username="superadmin",
            password="superadminpass",
            restaurant_slug="default_restaurant_slug",
            role=UserRole.SUPERADMIN
        )
        logger.info("Default superadmin user created (if not exists).")
    except ValueError as e:
        logger.info(f"Default superadmin user already exists: {e}")
    except Exception as e:
        logger.error(f"Error creating default superadmin user: {e}")

    yield
    # Shutdown
    logger.info("Shutting down Restaurant PWA Backend...")
    await close_db()
    logger.info("Database connection closed")

app = FastAPI(
    title="Restaurant PWA Backend",
    description="API for managing restaurant orders and products.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration
origins = [
    "http://localhost:3000",  # Frontend URL
    "http://localhost:8000",  # Backend URL
    # Add your deployed frontend URL here when you deploy
    # "https://your-frontend-url.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get ProductService
async def get_product_service():
    return ProductService(database)

app.include_router(products.router, prefix="/api", tags=["products"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the Restaurant PWA Backend!"}

# ===== AUTH ENDPOINTS =====
@app.post("/auth/login", response_model=TokenResponse, tags=["auth"])
async def login(login_data: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.authenticate_user(
        login_data.username,
        login_data.password,
        login_data.restaurant_slug
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result

@app.post("/auth/refresh", response_model=TokenResponse, tags=["auth"])
async def refresh_token(refresh_data: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.refresh_access_token(refresh_data.refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result

# Example of a protected route (requires authentication)
@app.get("/protected-test", tags=["test"])
async def protected_test(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}, you are authenticated!"}

# Example of an admin-protected route
@app.get("/admin-test", tags=["test"])
async def admin_test(current_user: dict = Depends(get_current_admin_user)):
    return {"message": f"Hello admin {current_user['username']}, you have admin access!"}