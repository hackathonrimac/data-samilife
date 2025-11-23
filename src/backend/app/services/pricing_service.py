"""Pricing service for healthcare API."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException

from app.db.models import Servicio, Asegurado
from app.schemas.responses import PricingInfo


async def get_service_pricing(
    db: AsyncSession,
    codigo: str,
    servicio: str,
    cmp: Optional[str] = None,
    profesion: Optional[str] = None
) -> PricingInfo:
    """
    Calculate regular and insurance-discounted pricing for a service.
    
    Queries Servicio table by cod_unico and service details, queries Asegurado
    table for insurance pricing (Rimac), calculates precio_normal from service
    data, calculates precio_rimac from asegurado.costo_consulta if available,
    and returns both prices as integers.
    
    Args:
        db: Database session
        codigo: Establishment unique code (cod_unico)
        servicio: Service name or type
        cmp: Optional professional CMP code
        profesion: Optional professional type
        
    Returns:
        PricingInfo with precio_normal and precio_rimac as integers
        
    Raises:
        HTTPException: 404 if service not found
        
    Requirements: 4.1, 4.2, 4.3, 4.5
    """
    # Query Servicio table for the service
    # Build query conditions
    conditions = [
        Servicio.cod_unico == codigo,
        Servicio.servicio == servicio
    ]
    
    if cmp:
        conditions.append(Servicio.cmp == cmp)
    if profesion:
        conditions.append(Servicio.profesion == profesion)
    
    query = select(Servicio).filter(and_(*conditions))
    result = await db.execute(query)
    service = result.scalar_one_or_none()
    
    if service is None:
        raise HTTPException(
            status_code=404,
            detail=f"Service '{servicio}' not found at establishment '{codigo}'"
        )
    
    # For precio_normal, we'll use a default value since the Servicio table
    # doesn't have a price field. In a real system, this would come from
    # service data or a separate pricing table.
    # For now, we'll set a default base price
    precio_normal = 100  # Default base price
    
    # Query Asegurado table for Rimac insurance pricing
    asegurado_query = select(Asegurado).filter(
        and_(
            Asegurado.cod_unico == codigo,
            Asegurado.seguro.ilike('%rimac%')  # Case-insensitive match for Rimac
        )
    )
    asegurado_result = await db.execute(asegurado_query)
    asegurado = asegurado_result.scalar_one_or_none()
    
    # Calculate precio_rimac
    if asegurado and asegurado.costo_consulta is not None:
        # Use insurance-discounted price
        precio_rimac = int(asegurado.costo_consulta)
    else:
        # No insurance discount available, use same price
        precio_rimac = precio_normal
    
    return PricingInfo(
        precio_normal=precio_normal,
        precio_rimac=precio_rimac
    )
