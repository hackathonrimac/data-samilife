"""Dynamic filter utilities for the healthcare API."""

from typing import Any, Dict, List
from sqlalchemy import Column
from sqlalchemy.orm import Query


class FilterValidationError(Exception):
    """Raised when filter structure is invalid."""
    pass


def validate_filter_structure(filters: Dict[str, Any]) -> None:
    """
    Validate the structure of filter criteria.
    
    Args:
        filters: Dictionary containing filter criteria
        
    Raises:
        FilterValidationError: If filter structure is invalid
        
    Requirements: 1.4
    """
    if not isinstance(filters, dict):
        raise FilterValidationError("Filters must be a dictionary")
    
    valid_operators = {'eq', 'ne', 'gt', 'lt', 'gte', 'lte', 'in', 'contains'}
    
    for field, criteria in filters.items():
        if not isinstance(field, str):
            raise FilterValidationError(f"Field name must be a string, got: {type(field)}")
        
        # Criteria can be a simple value (implies 'eq') or a dict with operator
        if isinstance(criteria, dict):
            # Check if it has an operator key
            if 'operator' in criteria:
                operator = criteria['operator']
                if operator not in valid_operators:
                    raise FilterValidationError(
                        f"Invalid operator '{operator}'. "
                        f"Valid operators: {', '.join(valid_operators)}"
                    )
                
                if 'value' not in criteria:
                    raise FilterValidationError(
                        f"Filter with operator must have 'value' key"
                    )
            else:
                # If no operator, treat the dict as the value (for nested objects)
                pass


def apply_dynamic_filters(
    query: Query,
    filters: Dict[str, Any],
    model_class: Any
) -> Query:
    """
    Apply dynamic filters to a SQLAlchemy query.
    
    Supports the following operators:
    - eq: Equal to (default if no operator specified)
    - ne: Not equal to
    - gt: Greater than
    - lt: Less than
    - gte: Greater than or equal to
    - lte: Less than or equal to
    - in: Value in list
    - contains: String contains substring (case-insensitive)
    
    Args:
        query: SQLAlchemy query object
        filters: Dictionary of filter criteria
        model_class: SQLAlchemy model class to filter on
        
    Returns:
        Modified query with filters applied
        
    Raises:
        FilterValidationError: If filter structure is invalid
        AttributeError: If field doesn't exist on model
        
    Requirements: 1.4
    
    Example:
        filters = {
            "direccion": {"operator": "contains", "value": "Lima"},
            "clasificacion": "Hospital",
            "calificacion": {"operator": "gte", "value": 4}
        }
    """
    # Validate filter structure first
    validate_filter_structure(filters)
    
    for field_name, criteria in filters.items():
        # Get the column from the model
        if not hasattr(model_class, field_name):
            raise AttributeError(
                f"Model {model_class.__name__} has no attribute '{field_name}'"
            )
        
        column: Column = getattr(model_class, field_name)
        
        # Parse criteria
        if isinstance(criteria, dict) and 'operator' in criteria:
            operator = criteria['operator']
            value = criteria['value']
        else:
            # Default to equality
            operator = 'eq'
            value = criteria
        
        # Apply the appropriate filter based on operator
        if operator == 'eq':
            query = query.filter(column == value)
        elif operator == 'ne':
            query = query.filter(column != value)
        elif operator == 'gt':
            query = query.filter(column > value)
        elif operator == 'lt':
            query = query.filter(column < value)
        elif operator == 'gte':
            query = query.filter(column >= value)
        elif operator == 'lte':
            query = query.filter(column <= value)
        elif operator == 'in':
            if not isinstance(value, (list, tuple)):
                raise FilterValidationError(
                    f"'in' operator requires a list or tuple, got: {type(value)}"
                )
            query = query.filter(column.in_(value))
        elif operator == 'contains':
            if not isinstance(value, str):
                raise FilterValidationError(
                    f"'contains' operator requires a string, got: {type(value)}"
                )
            # Case-insensitive contains
            query = query.filter(column.ilike(f"%{value}%"))
    
    return query
