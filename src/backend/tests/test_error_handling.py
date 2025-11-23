"""
Tests for error handling middleware.

Validates that the error handling middleware correctly catches and formats
various types of errors according to requirements.
"""

import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.exc import OperationalError

from app.main import app
from app.db.connection import get_db_session


# Mock database session for tests
async def mock_get_db_session():
    """Mock database session that doesn't require actual database connection."""
    mock_session = AsyncMock()
    yield mock_session


# Override the database dependency
app.dependency_overrides[get_db_session] = mock_get_db_session

client = TestClient(app)


def test_root_endpoint():
    """Test that the root endpoint works correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Healthcare API"
    assert response.json()["status"] == "running"


def test_404_not_found():
    """Test that 404 errors are handled correctly."""
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404


def test_validation_error_malformed_json():
    """
    Test that malformed JSON in filtros parameter returns HTTP 400.
    
    Requirements: 6.1, 8.3
    """
    response = client.get("/get?filtros={invalid json}")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data or "detail" in data


def test_validation_error_invalid_date():
    """
    Test that invalid date format returns HTTP 400.
    
    Requirements: 6.3, 8.3
    """
    response = client.get("/get?fecha=invalid-date")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data or "detail" in data


def test_error_response_no_credentials():
    """
    Test that error responses never contain credentials.
    
    Requirements: 7.3
    """
    # Test with various endpoints
    response = client.get("/get?filtros={invalid}")
    assert response.status_code == 400
    
    # Check that response doesn't contain sensitive data
    response_text = response.text.lower()
    
    # Check for common credential keywords
    assert "password" not in response_text or "[redacted]" in response_text.lower()
    
    # If DB_PASSWORD is set in environment, ensure it's not in the response
    db_password = os.getenv("DB_PASSWORD", "")
    if db_password:  # Only check if password is actually set
        assert db_password not in response_text


if __name__ == "__main__":
    import os
    pytest.main([__file__, "-v"])
