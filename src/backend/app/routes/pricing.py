"""Pricing routes for healthcare API."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.db.connection import get_db_session
from app.services.pricing_service import get_service_pricing
from app.schemas.responses import PricingInfo

router = APIRouter(prefix="", tags=["pricing"])


@router.get("/get/precio/cita", response_model=PricingInfo)
async def get_pricing_endpoint(
    codigo: str = Query(..., description="Establishment unique code (cod_unico)"),
    servicio: str = Query(..., description="Service details as JSON string"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get pricing information for a specific medical service.
    
    Requirements: 4.1, 4.2, 4.3, 4.5, 6.2
    """
    # Parse servicio JSON parameter
    try:
        servicio_dict = json.loads(servicio)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_ERROR",
                "message": "Invalid JSON in servicio parameter",
                "details": {
                    "field": "servicio",
                    "error": str(e)
                }
            }
        )
    
    # Validate required parameters in servicio
    if 'servicio' not in servicio_dict:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_ERROR",
                "message": "Missing required parameter 'servicio' in service details",
                "details": {
                    "field": "servicio",
                    "required": ["servicio"]
                }
            }
        )
    
    # Extract service details
    servicio_name = servicio_dict.get('servicio')
    cmp = servicio_dict.get('cmp')
    profesion = servicio_dict.get('profesion')
    
    try:
        pricing = await get_service_pricing(
            db=db,
            codigo=codigo,
            servicio=servicio_name,
            cmp=cmp,
            profesion=profesion
        )
        return pricing
    except HTTPException:
        # Re-raise HTTPExceptions (like 404) from service layer
        raise
    except Exception as e:
        # Log the error (logging will be implemented in task 10)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while retrieving pricing information"
            }
        )
