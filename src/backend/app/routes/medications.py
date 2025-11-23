"""Medication routes for healthcare API."""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.db.connection import get_db_session
from app.services.medication_service import search_medications
from app.schemas.responses import MedicationInfo

router = APIRouter(prefix="", tags=["medications"])


@router.get("/get/medicina", response_model=List[dict])
async def search_medicine_by_name(
    nombre: str = Query(..., description="Medicine name to search for"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Search for medicines by name across all establishments.
    Returns medicine information with establishments where it's available and stock.
    
    Query Parameters:
        nombre: Medicine name (partial match supported)
    
    Returns:
        List of medicines with establishment information and stock
    """
    from app.services.medication_service import search_medicine_by_name as search_service
    
    try:
        results = await search_service(db=db, nombre=nombre)
        return results
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error searching medicine by name: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": f"An unexpected error occurred while searching medicine: {type(e).__name__}"
            }
        )


@router.get("/get/{cod_unico}/farmacos", response_model=List[MedicationInfo])
async def search_medications_endpoint(
    cod_unico: str,
    filtros: Optional[str] = Query(None, description="JSON filters for medications"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Search for available medications at a specific establishment with filtering.
    
    Requirements: 5.1, 5.2, 5.3, 5.4, 6.1
    """
    # Parse filtros JSON if provided
    filtros_dict = None
    if filtros:
        try:
            filtros_dict = json.loads(filtros)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid JSON in filtros parameter",
                    "details": {
                        "field": "filtros",
                        "error": str(e)
                    }
                }
            )
    
    try:
        medications = await search_medications(
            db=db,
            cod_unico=cod_unico,
            filtros=filtros_dict
        )
        return medications
    except Exception as e:
        # Log the error (logging will be implemented in task 10)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while searching medications"
            }
        )
