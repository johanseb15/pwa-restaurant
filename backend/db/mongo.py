from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

database = None
database_name = os.getenv("DATABASE_NAME", "pedidos") # Default to 'pedidos' if not set

async def init_db():
    global database
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        logger.error("MONGO_URI environment variable not set.")
        raise ValueError("MONGO_URI environment variable not set.")
    
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        database = client[database_name]
        logger.info(f"Successfully connected to MongoDB: {database_name}")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise

async def close_db():
    global database
    if database:
        database.client.close()
        logger.info("MongoDB connection closed.")
