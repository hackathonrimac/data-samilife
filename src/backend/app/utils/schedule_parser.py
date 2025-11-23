"""Schedule parsing utilities for the healthcare API."""

import json
from datetime import datetime, time, timedelta
from typing import Any, Dict, List, Optional


class ScheduleEntry:
    """Represents a single schedule entry."""
    
    def __init__(self, dia: int, ini: str, fin: str):
        """
        Initialize a schedule entry.
        
        Args:
            dia: Day of month
            ini: Start datetime string (ISO format)
            fin: End datetime string (ISO format)
        """
        self.dia = dia
        self.ini = ini
        self.fin = fin
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "dia": self.dia,
            "ini": self.ini,
            "fin": self.fin
        }
    
    def __eq__(self, other):
        """Check equality with another ScheduleEntry."""
        if not isinstance(other, ScheduleEntry):
            return False
        return (self.dia == other.dia and 
                self.ini == other.ini and 
                self.fin == other.fin)


def parse_schedule_json(schedule_json: str) -> List[ScheduleEntry]:
    """
    Parse schedule JSON from the servicio.detalle field.
    
    Expected format:
    [
      {
        "dia": 22,
        "ini": "2025-11-22 19:00",
        "fin": "2025-11-22 23:55"
      },
      ...
    ]
    
    Args:
        schedule_json: JSON string containing schedule data
        
    Returns:
        List of ScheduleEntry objects
        
    Raises:
        ValueError: If JSON is malformed or doesn't match expected structure
        
    Requirements: 9.1, 9.4
    """
    if not schedule_json:
        raise ValueError("Schedule JSON cannot be empty")
    
    try:
        schedule_data = json.loads(schedule_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    
    if not isinstance(schedule_data, list):
        raise ValueError("Schedule data must be a JSON array")
    
    schedule_entries = []
    for entry in schedule_data:
        print(f"Processing schedule entry: {entry}")
        if not isinstance(entry, dict):
            raise ValueError("Each schedule entry must be a JSON object")
        
        # Validate required fields
        if "dia" not in entry or "ini" not in entry or "fin" not in entry:
            raise ValueError("Schedule entry must contain 'dia', 'ini', and 'fin' fields")
        
        # Validate field types
        if not isinstance(entry["dia"], int):
            raise ValueError("Field 'dia' must be an integer")
        if not isinstance(entry["ini"], str):
            raise ValueError("Field 'ini' must be a string")
        if not isinstance(entry["fin"], str):
            raise ValueError("Field 'fin' must be a string")
        
        schedule_entries.append(
            ScheduleEntry(
                dia=entry["dia"],
                ini=entry["ini"],
                fin=entry["fin"]
            )
        )
    
    return schedule_entries


def serialize_schedule(schedule_entries: List[ScheduleEntry]) -> str:
    """
    Serialize schedule entries to JSON string.
    
    Args:
        schedule_entries: List of ScheduleEntry objects
        
    Returns:
        JSON string representation
    """
    schedule_list = [entry.to_dict() for entry in schedule_entries]
    return json.dumps(schedule_list)


def is_available_on_date(schedule_entries: List[ScheduleEntry], target_date: datetime) -> bool:
    """
    Check if a service is available on a given date.
    
    Args:
        schedule_entries: List of ScheduleEntry objects
        target_date: The date to check availability for
        
    Returns:
        True if service is available on the target date, False otherwise
        
    Requirements: 9.2
    """
    if not schedule_entries:
        return False
    
    target_day = target_date.day
    
    for entry in schedule_entries:
        # Check if the schedule entry is for the target day
        if entry.dia == target_day:
            return True
        
        # Check for midnight-spanning schedules
        try:
            ini_dt = datetime.fromisoformat(entry.ini.replace(' ', 'T'))
            fin_dt = datetime.fromisoformat(entry.fin.replace(' ', 'T'))
            
            # If end time is before start time, it spans midnight
            if fin_dt < ini_dt:
                # Check if target date matches either the start or end date
                if target_day == ini_dt.day or target_day == fin_dt.day:
                    return True
        except (ValueError, AttributeError):
            # If datetime parsing fails, skip this entry
            continue
    
    return False


def handle_midnight_spanning(ini: str, fin: str) -> bool:
    """
    Determine if a schedule spans midnight.
    
    Args:
        ini: Start datetime string (ISO format)
        fin: End datetime string (ISO format)
        
    Returns:
        True if the schedule spans midnight, False otherwise
        
    Requirements: 9.2
    """
    try:
        # Parse datetime strings (handle both space and T separators)
        ini_dt = datetime.fromisoformat(ini.replace(' ', 'T'))
        fin_dt = datetime.fromisoformat(fin.replace(' ', 'T'))
        
        # If end datetime is before or equal to start datetime, it spans midnight
        # or crosses into the next day
        return fin_dt <= ini_dt or fin_dt.date() > ini_dt.date()
    except (ValueError, AttributeError):
        # If parsing fails, assume it doesn't span midnight
        return False


def parse_schedule_safe(schedule_json: str) -> Optional[List[ScheduleEntry]]:
    """
    Safely parse schedule JSON, returning None if malformed.
    
    This function handles malformed JSON gracefully without raising exceptions.
    
    Args:
        schedule_json: JSON string containing schedule data
        
    Returns:
        List of ScheduleEntry objects, or None if parsing fails
        
    Requirements: 9.5
    """
    try:
        return parse_schedule_json(schedule_json)
    except (ValueError, json.JSONDecodeError, KeyError, TypeError):
        # Return None for any parsing errors
        return None
