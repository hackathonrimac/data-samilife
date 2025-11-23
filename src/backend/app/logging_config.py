"""
Structured logging configuration for the healthcare API.

This module configures Python logging with JSON formatting, log rotation,
and sensitive data filtering.

Requirements: 10.1, 10.2, 10.3, 10.4, 10.5
"""

import logging
import logging.handlers
import json
import os
import re
from datetime import datetime
from typing import Any, Dict
from pathlib import Path


# Sensitive data patterns to filter from logs
SENSITIVE_PATTERNS = [
    r'password["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
    r'pwd["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
    r'token["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
    r'api_key["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
    r'secret["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
    r'authorization["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
    r'DB_PASSWORD["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
    r'DB_USER["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
]

# Health data patterns (common medical identifiers)
HEALTH_DATA_PATTERNS = [
    r'\b\d{3}-\d{2}-\d{4}\b',  # SSN-like patterns
    r'\bDNI[:\s]*\d{8}\b',  # DNI numbers
    r'\bhistoria[_\s]clinica[:\s]*\d+\b',  # Medical record numbers
]


class SensitiveDataFilter(logging.Filter):
    """
    Filter to remove sensitive information from log records.
    
    Filters out passwords, tokens, API keys, personal health data,
    and other sensitive information before logging.
    
    Requirements: 10.3
    """
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter sensitive data from log record."""
        # Filter message
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = self._sanitize_text(record.msg)
        
        # Filter args
        if hasattr(record, 'args') and record.args:
            if isinstance(record.args, dict):
                record.args = {k: self._sanitize_value(v) for k, v in record.args.items()}
            elif isinstance(record.args, (list, tuple)):
                record.args = tuple(self._sanitize_value(arg) for arg in record.args)
        
        # Filter extra fields
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName', 
                              'levelname', 'levelno', 'lineno', 'module', 'msecs', 
                              'pathname', 'process', 'processName', 'relativeCreated', 
                              'thread', 'threadName', 'exc_info', 'exc_text', 'stack_info']:
                    if isinstance(value, str):
                        setattr(record, key, self._sanitize_text(value))
                    elif isinstance(value, dict):
                        setattr(record, key, {k: self._sanitize_value(v) for k, v in value.items()})
        
        return True
    
    def _sanitize_text(self, text: str) -> str:
        """Remove sensitive patterns from text."""
        sanitized = text
        
        # Filter sensitive credentials
        for pattern in SENSITIVE_PATTERNS:
            sanitized = re.sub(pattern, r'\1[REDACTED]', sanitized, flags=re.IGNORECASE)
        
        # Filter health data
        for pattern in HEALTH_DATA_PATTERNS:
            sanitized = re.sub(pattern, '[HEALTH_DATA_REDACTED]', sanitized, flags=re.IGNORECASE)
        
        # Also filter environment variable values
        db_password = os.getenv("DB_PASSWORD", "")
        db_user = os.getenv("DB_USER", "")
        if db_password and db_password in sanitized:
            sanitized = sanitized.replace(db_password, "[REDACTED]")
        if db_user and db_user in sanitized:
            sanitized = sanitized.replace(db_user, "[REDACTED]")
        
        return sanitized
    
    def _sanitize_value(self, value: Any) -> Any:
        """Sanitize a value recursively."""
        if isinstance(value, str):
            return self._sanitize_text(value)
        elif isinstance(value, dict):
            return {k: self._sanitize_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return type(value)(self._sanitize_value(item) for item in value)
        return value


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    Formats log records as JSON objects with consistent structure
    for easy parsing and analysis.
    
    Requirements: 10.1, 10.2, 10.4
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields from record
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName', 
                          'levelname', 'levelno', 'lineno', 'module', 'msecs', 
                          'pathname', 'process', 'processName', 'relativeCreated', 
                          'thread', 'threadName', 'exc_info', 'exc_text', 'stack_info',
                          'getMessage', 'message']:
                extra_fields[key] = value
        
        if extra_fields:
            log_data["extra"] = extra_fields
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info) if record.exc_info else None,
            }
        
        # Add stack trace if present
        if record.stack_info:
            log_data["stack_trace"] = record.stack_info
        
        return json.dumps(log_data)


async def request_logging_middleware(request, call_next):
    """
    Middleware to log all incoming requests.
    
    Logs endpoint, parameters, timestamp, and other request metadata
    for monitoring and debugging.
    
    Requirements: 10.1
    """
    logger = logging.getLogger("app.requests")
    
    # Extract request information
    method = request.method
    path = request.url.path
    query_params = str(request.query_params)
    client_host = request.client.host if request.client else None
    
    # Log request
    logger.info(
        f"Request: {method} {path}",
        extra={
            "endpoint": path,
            "method": method,
            "query_params": query_params,
            "client_host": client_host,
        }
    )
    
    # Process request
    response = await call_next(request)
    
    # Log response status
    logger.info(
        f"Response: {method} {path} - {response.status_code}",
        extra={
            "endpoint": path,
            "method": method,
            "status_code": response.status_code,
        }
    )
    
    return response


def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "logs",
    enable_console: bool = True,
    enable_file: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
) -> None:
    """
    Configure structured logging for the application.
    
    Sets up JSON-formatted logging with rotation, sensitive data filtering,
    and appropriate log levels.
    
    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR)
        log_dir: Directory for log files
        enable_console: Whether to log to console
        enable_file: Whether to log to file
        max_bytes: Maximum size of each log file before rotation
        backup_count: Number of backup log files to keep
    
    Requirements: 10.1, 10.2, 10.3, 10.4, 10.5
    """
    # Create log directory if it doesn't exist
    if enable_file:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    json_formatter = JSONFormatter()
    
    # Create sensitive data filter
    sensitive_filter = SensitiveDataFilter()
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(json_formatter)
        console_handler.addFilter(sensitive_filter)
        root_logger.addHandler(console_handler)
    
    # File handler with rotation
    if enable_file:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(log_dir, "app.log"),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(json_formatter)
        file_handler.addFilter(sensitive_filter)
        root_logger.addHandler(file_handler)
        
        # Separate error log file
        error_handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(log_dir, "error.log"),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(json_formatter)
        error_handler.addFilter(sensitive_filter)
        root_logger.addHandler(error_handler)
    
    # Configure specific loggers
    logging.getLogger("app").setLevel(getattr(logging, log_level.upper()))
    logging.getLogger("app.requests").setLevel(logging.INFO)
    logging.getLogger("app.errors").setLevel(logging.WARNING)
    
    # Suppress noisy third-party loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("asyncpg").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    root_logger.info(
        "Logging configured",
        extra={
            "log_level": log_level,
            "console_enabled": enable_console,
            "file_enabled": enable_file,
            "log_directory": log_dir,
        }
    )
