"""
Healthcare API - FastAPI Application Entry Point

This module initializes the FastAPI application and configures
routes, middleware, and lifecycle events.
"""

import os
import logging
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.routes import establishments, appointments, pricing, medications
from app.middleware.error_handler import error_handler_middleware
from app.db.connection import init_db, close_db
from app.logging_config import setup_logging, request_logging_middleware

# Initialize logging
setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_dir=os.getenv("LOG_DIR", "logs"),
    enable_console=True,
    enable_file=True,
)

logger = logging.getLogger(__name__)

# Application metadata
app = FastAPI(
    title="Healthcare API",
    description="API for healthcare facility search, appointments, pricing, and medications",
    version="1.0.0",
)

# Request logging middleware
app.middleware("http")(request_logging_middleware)

# Error handling middleware (must be added after request logging to catch all errors)
app.middleware("http")(error_handler_middleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(establishments.router)
app.include_router(appointments.router)
app.include_router(pricing.router)
app.include_router(medications.router)


@app.on_event("startup")
async def startup_event():
    """Initialize resources on application startup"""
    logger.info("Starting Healthcare API application")
    await init_db()
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on application shutdown"""
    logger.info("Shutting down Healthcare API application")
    await close_db()
    logger.info("Application shutdown complete")


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Healthcare API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancer monitoring.
    
    Returns:
        200 if healthy with version information
        503 if unhealthy (database connectivity issues)
    
    Requirements: 7.1
    """
    from app.db.connection import engine
    from sqlalchemy import text
    
    health_status = {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Healthcare API"
    }
    
    # Check database connectivity
    if engine is None:
        health_status["status"] = "unhealthy"
        health_status["database"] = "not initialized"
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_status
        )
    
    try:
        # Test database connection
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        
        health_status["database"] = "connected"
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=health_status
        )
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        health_status["status"] = "unhealthy"
        health_status["database"] = "connection failed"
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_status
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
