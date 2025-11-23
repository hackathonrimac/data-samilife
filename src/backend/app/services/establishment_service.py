"""Establishment service for healthcare API."""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.db.models import Institucion, Servicio, Profesional, Asegurado
from app.schemas.responses import (
    EstablishmentSummary,
    EstablishmentInfo,
    ServiceInfo,
    ProfessionalInfo,
    InsuranceInfo
)
from app.utils.filters import apply_dynamic_filters
from app.utils.schedule_parser import parse_schedule_safe, is_available_on_date
from datetime import datetime


async def search_establishments(
    db: AsyncSession,
    lugar: Optional[str] = None,
    fecha: Optional[str] = None,
    tipo: Optional[str] = None,
    filtros: Optional[Dict[str, Any]] = None
) -> List[EstablishmentSummary]:
    """
    Search for healthcare establishments with multiple filter criteria.
    
    Implements location filtering by direccion field, date filtering by checking
    service schedules, type filtering by institucion field (público/privado),
    and applies custom JSON filters.
    
    Args:
        db: Database session
        lugar: Location/address to filter by (partial match)
        fecha: Date in YYYY-MM-DD format to check service availability
        tipo: Institution type (público/privado)
        filtros: Custom JSON filters to apply
        
    Returns:
        List of EstablishmentSummary objects
        
    Requirements: 1.1, 1.2, 1.3, 1.4, 1.5
    """
    # Start with base query
    query = select(Institucion)
    
    # Apply location filter (case-insensitive partial match)
    if lugar:
        query = query.filter(Institucion.direccion.ilike(f"%{lugar}%"))
    
    # Apply type filter
    if tipo:
        query = query.filter(Institucion.institucion == tipo)
    
    # Apply custom JSON filters
    if filtros:
        query = apply_dynamic_filters(query, filtros, Institucion)
    
    # Execute query
    result = await db.execute(query)
    establishments = result.scalars().all()
    
    # If date filter is provided, filter by service availability
    if fecha:
        try:
            target_date = datetime.fromisoformat(fecha)
            filtered_establishments = []
            
            for establishment in establishments:
                # Load services for this establishment
                services_query = select(Servicio).filter(
                    Servicio.cod_unico == establishment.cod_unico
                )
                services_result = await db.execute(services_query)
                services = services_result.scalars().all()
                
                # Check if any service is available on the target date
                has_availability = False
                for service in services:
                    if service.detalle:
                        schedule_entries = parse_schedule_safe(service.detalle)
                        if schedule_entries and is_available_on_date(schedule_entries, target_date):
                            has_availability = True
                            break
                
                if has_availability:
                    filtered_establishments.append(establishment)
            
            establishments = filtered_establishments
        except ValueError:
            # Invalid date format - skip date filtering
            pass
    
    # Convert to EstablishmentSummary objects
    summaries = []
    for est in establishments:
        summaries.append(
            EstablishmentSummary(
                nombre=est.establecimiento,
                direccion=est.direccion,
                calificacion=est.clasificacion,
                cod_unico=est.cod_unico
            )
        )
    
    return summaries


async def get_establishment_info(
    db: AsyncSession,
    cod_unico: str
) -> EstablishmentInfo:
    """
    Retrieve complete establishment information with all associated data.
    
    Queries Institucion by cod_unico and eager loads related services,
    professionals, and insurance coverage.
    
    Args:
        db: Database session
        cod_unico: Unique establishment identifier
        
    Returns:
        EstablishmentInfo with all associated data
        
    Raises:
        HTTPException: 404 if cod_unico not found
        
    Requirements: 2.1, 2.2, 2.3, 2.4
    """
    # Query with eager loading of relationships
    query = (
        select(Institucion)
        .options(
            selectinload(Institucion.servicios).selectinload(Servicio.profesional_rel),
            selectinload(Institucion.seguros)
        )
        .filter(Institucion.cod_unico == cod_unico)
    )
    
    result = await db.execute(query)
    establishment = result.scalar_one_or_none()
    
    # Raise 404 if not found
    if establishment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Establishment with cod_unico '{cod_unico}' not found"
        )
    
    # Build service information
    services = []
    professionals_dict = {}  # Use dict to avoid duplicates
    
    for servicio in establishment.servicios:
        services.append(
            ServiceInfo(
                servicio=servicio.servicio,
                profesional=servicio.profesional_rel.nombre_profesional if servicio.profesional_rel else None,
                especialidad=servicio.profesional_rel.especialidad if servicio.profesional_rel else None,
                telefono=servicio.telefono
            )
        )
        
        # Collect unique professionals
        if servicio.profesional_rel:
            prof = servicio.profesional_rel
            key = (prof.cmp, prof.profesion)
            if key not in professionals_dict:
                professionals_dict[key] = ProfessionalInfo(
                    cmp=prof.cmp,
                    nombre=prof.nombre_profesional,
                    profesion=prof.profesion,
                    especialidad=prof.especialidad
                )
    
    # Build insurance information
    seguros = []
    for asegurado in establishment.seguros:
        seguros.append(
            InsuranceInfo(
                seguro=asegurado.seguro,
                red=asegurado.red,
                costo_consulta=asegurado.costo_consulta
            )
        )
    
    # Build complete establishment info
    return EstablishmentInfo(
        cod_unico=establishment.cod_unico,
        nombre=establishment.establecimiento,
        direccion=establishment.direccion,
        institucion=establishment.institucion,
        establecimiento=establishment.establecimiento,
        clasificacion=establishment.clasificacion,
        correo=establishment.correo,
        longitud=establishment.longitud,
        latitud=establishment.latitud,
        pagina=establishment.pagina,
        servicios=services,
        profesionales=list(professionals_dict.values()),
        seguros=seguros
    )
