"""Appointment service for healthcare API."""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.db.models import Servicio, Profesional
from app.schemas.responses import AppointmentSlot, ScheduleEntry
from app.utils.schedule_parser import parse_schedule_safe, is_available_on_date


async def get_available_appointments(
    db: AsyncSession,
    cod_unico: str,
    filtros: Optional[Dict[str, Any]] = None
) -> List[AppointmentSlot]:
    """
    Get available appointment slots for a specific establishment with filtering.
    
    Queries Servicio table by cod_unico, parses detalle JSON field for each service,
    applies filters (specialty, professional, date range, service type), joins with
    Profesional to get professional details, and returns list of AppointmentSlot objects.
    
    Args:
        db: Database session
        cod_unico: Unique establishment identifier
        filtros: Optional filters including:
            - especialidad: Medical specialty filter
            - profesional: Professional name or CMP filter
            - fecha_inicio: Start date for range (YYYY-MM-DD)
            - fecha_fin: End date for range (YYYY-MM-DD)
            - tipo_servicio: Service type filter
        
    Returns:
        List of AppointmentSlot objects with schedule details
        
    Requirements: 3.1, 3.2, 3.3, 3.4, 3.5
    """
    # Build query with eager loading of professional relationship
    query = (
        select(Servicio)
        .options(selectinload(Servicio.profesional_rel))
        .filter(Servicio.cod_unico == cod_unico)
    )
    
    # Execute query
    result = await db.execute(query)
    services = result.scalars().all()
    
    # Parse filters
    especialidad_filter = None
    profesional_filter = None
    fecha_inicio = None
    fecha_fin = None
    tipo_servicio_filter = None
    
    if filtros:
        especialidad_filter = filtros.get('especialidad')
        profesional_filter = filtros.get('profesional')
        tipo_servicio_filter = filtros.get('tipo_servicio')
        
        # Parse date filters
        if 'fecha_inicio' in filtros and filtros['fecha_inicio']:
            try:
                fecha_inicio = datetime.fromisoformat(filtros['fecha_inicio'])
            except (ValueError, TypeError):
                pass
        
        if 'fecha_fin' in filtros and filtros['fecha_fin']:
            try:
                fecha_fin = datetime.fromisoformat(filtros['fecha_fin'])
            except (ValueError, TypeError):
                pass
    
    # Process services and build appointment slots
    appointment_slots = []
    
    for service in services:
        # Parse schedule from detalle field
        if not service.detalle:
            continue
        
        schedule_entries = parse_schedule_safe(service.detalle)
        if not schedule_entries:
            # Skip services with malformed schedules
            continue
        
        # Get professional details
        professional = service.profesional_rel
        if not professional:
            continue
        
        # Apply specialty filter
        if especialidad_filter:
            if not professional.especialidad or especialidad_filter.lower() not in professional.especialidad.lower():
                continue
        
        # Apply professional filter (match against name or CMP)
        if profesional_filter:
            match_name = professional.nombre_profesional and profesional_filter.lower() in professional.nombre_profesional.lower()
            match_cmp = professional.cmp and profesional_filter.lower() in professional.cmp.lower()
            if not (match_name or match_cmp):
                continue
        
        # Apply service type filter
        if tipo_servicio_filter:
            if not service.servicio or tipo_servicio_filter.lower() not in service.servicio.lower():
                continue
        
        # Apply date range filter
        if fecha_inicio or fecha_fin:
            # Check if any schedule entry falls within the date range
            has_match = False
            
            for entry in schedule_entries:
                try:
                    # Parse the entry dates
                    entry_ini = datetime.fromisoformat(entry.ini.replace(' ', 'T'))
                    entry_fin = datetime.fromisoformat(entry.fin.replace(' ', 'T'))
                    
                    # Check if entry overlaps with requested date range
                    if fecha_inicio and fecha_fin:
                        # Both start and end dates specified
                        if entry_ini.date() <= fecha_fin.date() and entry_fin.date() >= fecha_inicio.date():
                            has_match = True
                            break
                    elif fecha_inicio:
                        # Only start date specified
                        if entry_fin.date() >= fecha_inicio.date():
                            has_match = True
                            break
                    elif fecha_fin:
                        # Only end date specified
                        if entry_ini.date() <= fecha_fin.date():
                            has_match = True
                            break
                except (ValueError, AttributeError):
                    # Skip entries with invalid dates
                    continue
            
            if not has_match:
                continue
        
        # Convert schedule entries to response format
        schedule_response = [
            ScheduleEntry(
                dia=entry.dia,
                ini=entry.ini,
                fin=entry.fin
            )
            for entry in schedule_entries
        ]
        
        # Create appointment slot
        appointment_slot = AppointmentSlot(
            profesional=professional.nombre_profesional,
            cmp=professional.cmp,
            especialidad=professional.especialidad,
            servicio=service.servicio,
            horario=schedule_response,
            telefono=service.telefono
        )
        
        appointment_slots.append(appointment_slot)
    
    return appointment_slots
