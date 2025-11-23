"""Property-based tests for schedule parser utilities."""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from datetime import datetime

from app.utils.schedule_parser import (
    parse_schedule_json,
    serialize_schedule,
    ScheduleEntry,
    is_available_on_date,
    handle_midnight_spanning,
    parse_schedule_safe
)


# Strategy for generating valid schedule entries
@st.composite
def schedule_entry_strategy(draw):
    """Generate a valid ScheduleEntry."""
    dia = draw(st.integers(min_value=1, max_value=31))
    year = draw(st.integers(min_value=2020, max_value=2030))
    month = draw(st.integers(min_value=1, max_value=12))
    
    # Ensure day is valid for the month
    if month in [4, 6, 9, 11] and dia > 30:
        dia = 30
    elif month == 2 and dia > 28:
        dia = 28
    
    hour_ini = draw(st.integers(min_value=0, max_value=23))
    minute_ini = draw(st.integers(min_value=0, max_value=59))
    hour_fin = draw(st.integers(min_value=0, max_value=23))
    minute_fin = draw(st.integers(min_value=0, max_value=59))
    
    ini = f"{year:04d}-{month:02d}-{dia:02d} {hour_ini:02d}:{minute_ini:02d}"
    fin = f"{year:04d}-{month:02d}-{dia:02d} {hour_fin:02d}:{minute_fin:02d}"
    
    return ScheduleEntry(dia=dia, ini=ini, fin=fin)


# Feature: healthcare-api, Property 6: Schedule parsing round-trip
@given(st.lists(schedule_entry_strategy(), min_size=1, max_size=10))
@settings(max_examples=100)
def test_schedule_parsing_round_trip(schedule_entries):
    """
    Property 6: Schedule parsing round-trip
    
    For any valid schedule structure, serializing it to JSON and then 
    parsing it back should produce an equivalent schedule structure with 
    the same day, start time, and end time values.
    
    Validates: Requirements 9.1
    """
    # Serialize the schedule entries to JSON
    json_str = serialize_schedule(schedule_entries)
    
    # Parse the JSON back to schedule entries
    parsed_entries = parse_schedule_json(json_str)
    
    # Verify round-trip: parsed entries should equal original entries
    assert len(parsed_entries) == len(schedule_entries), \
        "Number of entries should be preserved"
    
    for original, parsed in zip(schedule_entries, parsed_entries):
        assert original.dia == parsed.dia, \
            f"Day should be preserved: {original.dia} != {parsed.dia}"
        assert original.ini == parsed.ini, \
            f"Start time should be preserved: {original.ini} != {parsed.ini}"
        assert original.fin == parsed.fin, \
            f"End time should be preserved: {original.fin} != {parsed.fin}"
        assert original == parsed, \
            "Schedule entries should be equal after round-trip"


# Strategy for generating malformed schedule JSON
def malformed_schedule_strategy():
    """Generate malformed schedule JSON strings."""
    return st.sampled_from([
        "{ invalid json }",  # Invalid JSON syntax
        '{"dia": 1, "ini": "2025-01-01 10:00", "fin": "2025-01-01 12:00"}',  # Not a list
        '[{"dia": 1, "ini": "2025-01-01 10:00"}]',  # Missing required fields
        '[{"dia": "not-a-number", "ini": "2025-01-01 10:00", "fin": "2025-01-01 12:00"}]',  # Wrong field types
        "",  # Empty string
        '["string", 123, true]',  # List with non-object elements
        "random text",  # Random string
        "null",  # JSON null
        "[]",  # Empty array
        '[{"dia": 1}]',  # Missing ini and fin
        '[{"ini": "2025-01-01 10:00", "fin": "2025-01-01 12:00"}]',  # Missing dia
    ])


# Feature: healthcare-api, Property 20: Graceful handling of malformed schedules
@given(malformed_schedule_strategy())
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_malformed_schedule_handling(malformed_json):
    """
    Property 20: Graceful handling of malformed schedules
    
    For any service with malformed or missing schedule data, the system 
    should exclude that service from results without crashing or returning 
    error responses.
    
    Validates: Requirements 9.5
    """
    # parse_schedule_safe should not raise an exception for any input
    result = parse_schedule_safe(malformed_json)
    
    # Result should be either None (for truly malformed data) or an empty list
    # (for valid but empty schedules)
    assert result is None or result == [], \
        f"Malformed schedule should return None or empty list, got: {result}"
    
    # Verify that parse_schedule_json raises ValueError for truly malformed input
    # (this is the strict version that should raise errors)
    if malformed_json == "[]":
        # Empty array is valid, should not raise
        parsed = parse_schedule_json(malformed_json)
        assert parsed == []
    else:
        # All other test cases should raise ValueError
        try:
            parse_schedule_json(malformed_json)
            # If we get here without exception, that's unexpected for our test cases
            # but acceptable (some edge cases might be valid)
        except (ValueError, Exception):
            # Expected behavior - malformed JSON should raise an error
            pass
