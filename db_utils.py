from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "resume_analysis_db")

# Global client variable
db_client: AsyncIOMotorClient | None = None


async def connect_to_mongo():
    """Establishes the connection to MongoDB when the application starts."""
    global db_client
    try:
        db_client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        # Force a connection attempt
        await db_client.admin.command("ping")
        print(f"✅ Connected to MongoDB: {MONGO_DB_NAME}")
    except Exception as e:
        print(f"❌ Could not connect to MongoDB: {e}")


async def close_mongo_connection():
    """Closes the MongoDB connection when the application shuts down."""
    global db_client
    if db_client:
        db_client.close()
        print("🛑 MongoDB connection closed.")


def get_database():
    """Returns the specific database instance."""
    global db_client
    if db_client:
        return db_client[MONGO_DB_NAME]
    raise ConnectionError("MongoDB client is not initialized.")
