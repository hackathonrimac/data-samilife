"""Database connection management with async support."""

import os
import logging
import asyncio
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Global engine and session factory
engine = None
async_session_factory = None

# Retry configuration
MAX_RETRIES = 3
INITIAL_BACKOFF = 1  # seconds


def get_database_url() -> str:
    """Construct database URL from environment variables."""
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")
    
    if not all([db_user, db_password, db_host, db_name]):
        raise ValueError(
            "Missing required database credentials. "
            "Please set DB_USER, DB_PASSWORD, DB_HOST, and DB_NAME environment variables."
        )
    
    return f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def sanitize_error_message(error_msg: str) -> str:
    """Remove sensitive information from error messages."""
    if not error_msg:
        return error_msg
    
    # Remove potential credentials from connection strings
    sensitive_patterns = [
        (os.getenv("DB_PASSWORD", ""), "[REDACTED_PASSWORD]"),
        (os.getenv("DB_USER", ""), "[REDACTED_USER]"),
    ]
    
    sanitized = error_msg
    for pattern, replacement in sensitive_patterns:
        if pattern and len(pattern) > 0:
            sanitized = sanitized.replace(pattern, replacement)
    
    return sanitized


async def init_db() -> None:
    """Initialize database connection pool on startup with retry logic."""
    global engine, async_session_factory
    
    database_url = get_database_url()
    
    for attempt in range(MAX_RETRIES):
        try:
            # Create async engine with connection pooling
            engine = create_async_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=20,
                max_overflow=10,
                pool_timeout=30,
                pool_pre_ping=True,  # Verify connections before using
                echo=False,  # Set to True for SQL query logging
            )
            
            # Test the connection
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            
            # Create session factory
            async_session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            
            logger.info("Database connection pool initialized successfully")
            return
            
        except (OperationalError, Exception) as e:
            # Log error without exposing credentials
            error_msg = sanitize_error_message(str(e))
            
            if attempt < MAX_RETRIES - 1:
                backoff_time = INITIAL_BACKOFF * (2 ** attempt)
                logger.warning(
                    f"Database connection attempt {attempt + 1}/{MAX_RETRIES} failed: {error_msg}. "
                    f"Retrying in {backoff_time} seconds..."
                )
                await asyncio.sleep(backoff_time)
            else:
                logger.error(
                    f"Failed to initialize database after {MAX_RETRIES} attempts: {error_msg}"
                )
                raise RuntimeError("Database connection failed after maximum retries")


async def close_db() -> None:
    """Close database connections on shutdown."""
    global engine
    
    if engine:
        try:
            await engine.dispose()
            logger.info("Database connections closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connections: {str(e)}")
            raise


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for route handlers to get database session.
    
    Usage in FastAPI routes:
        @app.get("/endpoint")
        async def endpoint(db: AsyncSession = Depends(get_db_session)):
            # Use db session here
    """
    if async_session_factory is None:
        raise RuntimeError(
            "Database not initialized. Call init_db() before using get_db_session()."
        )
    
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            # Log the full error for debugging, sanitize for external exposure
            logger.error(f"Database session error: {type(e).__name__}: {str(e)}")
            # Sanitize error message before re-raising
            error_msg = sanitize_error_message(str(e))
            # Re-raise with sanitized message if it contains sensitive data
            if error_msg != str(e):
                raise type(e)(error_msg) from e
            raise
