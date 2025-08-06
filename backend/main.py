from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import logging

from db.mongo import init_db, close_db, database
from routers import products
from services.products import ProductService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Validate required environment variables
required_vars = ["MONGO_URI", "SECRET_KEY", "DATABASE_NAME"]
for var in required_vars:
    if not os.getenv(var):
        raise RuntimeError(f"Missing required environment variable: {var}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Restaurant PWA Backend...")
    await init_db()
    logger.info("Database connection established")
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
# This function is now defined in main.py to be accessible by the router
async def get_product_service():
    return ProductService(database)

app.include_router(products.router, prefix="/api", tags=["products"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the Restaurant PWA Backend!"}
