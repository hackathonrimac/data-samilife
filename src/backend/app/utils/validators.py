"""Input validation utilities for the healthcare API."""

import re
from datetime import datetime
from typing import Any


def validate_cod_unico(cod_unico: str) -> bool:
    """
    Validate the format of a cod_unico (establishment code).
    
    Args:
        cod_unico: The establishment code to validate
        
    Returns:
        True if valid, False otherwise
        
    Requirements: 6.4
    """
    if not cod_unico or not isinstance(cod_unico, str):
        return False
    
    # cod_unico should be a non-empty string with alphanumeric characters
    # Based on typical IPRESS codes, they are usually numeric or alphanumeric
    # Allow alphanumeric, hyphens, and underscores
    pattern = r'^[A-Za-z0-9_-]+$'
    return bool(re.match(pattern, cod_unico)) and len(cod_unico) > 0


def validate_date_format(date_str: str) -> datetime:
    """
    Validate and parse a date string.
    
    Args:
        date_str: Date string to validate (expected format: YYYY-MM-DD)
        
    Returns:
        Parsed datetime object
        
    Raises:
        ValueError: If date format is invalid
        
    Requirements: 6.3
    """
    if not date_str or not isinstance(date_str, str):
        raise ValueError("Date must be a non-empty string")
    
    # Try to parse the date in YYYY-MM-DD format
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        return parsed_date
    except ValueError:
        raise ValueError(
            f"Invalid date format: '{date_str}'. Expected format: YYYY-MM-DD"
        )


def sanitize_input(input_value: Any) -> Any:
    """
    Sanitize input to prevent SQL injection attacks.
    
    This function removes or escapes potentially dangerous SQL characters
    and patterns from user input.
    
    Args:
        input_value: The input value to sanitize
        
    Returns:
        Sanitized input value
        
    Requirements: 6.5
    """
    if input_value is None:
        return None
    
    # If it's not a string, return as-is (numbers, booleans, etc. are safe)
    if not isinstance(input_value, str):
        return input_value
    
    # List of SQL injection patterns to detect
    sql_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|DECLARE)\b)",
        r"(--|;|\/\*|\*\/)",  # SQL comments and statement terminators
        r"(\bOR\b.*=.*)",  # OR-based injection patterns
        r"('.*--)",  # Quote-based comment injection
    ]
    
    # Check for SQL injection patterns (case-insensitive)
    for pattern in sql_patterns:
        if re.search(pattern, input_value, re.IGNORECASE):
            # If SQL injection pattern detected, escape single quotes
            # and remove dangerous characters
            sanitized = input_value.replace("'", "''")
            sanitized = re.sub(r'[;]', '', sanitized)
            sanitized = re.sub(r'--', '', sanitized)
            sanitized = re.sub(r'/\*|\*/', '', sanitized)
            return sanitized
    
    # For normal strings, just escape single quotes for SQL safety
    return input_value.replace("'", "''")
