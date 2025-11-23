"""Establishment routes for healthcare API."""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.db.connection import get_db_session
from app.services.establishment_service import search_establishments, get_establishment_info
from app.schemas.responses import EstablishmentSummary, EstablishmentInfo, ErrorResponse

router = APIRouter(prefix="", tags=["establishments"])


@router.get("/get", response_model=List[EstablishmentSummary])
async def search_establishments_endpoint(
    lugar: Optional[str] = Query(None, description="Location/address to filter by"),
    fecha: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    tipo: Optional[str] = Query(None, description="Institution type (público/privado)"),
    filtros: Optional[str] = Query(None, description="Custom JSON filters"),
    page: int = Query(1, ge=1, description="Page number for pagination (10 results per page)"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Search for healthcare establishments with multiple filter criteria.
    
    Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 6.1, 6.2, 8.1, 8.2, 8.3
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
    
    # Validate fecha format if provided
    if fecha:
        try:
            from datetime import datetime
            datetime.fromisoformat(fecha)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid date format provided",
                    "details": {
                        "field": "fecha",
                        "expected": "YYYY-MM-DD",
                        "received": fecha
                    }
                }
            )
    
    try:
        results = await search_establishments(
            db=db,
            lugar=lugar,
            fecha=fecha,
            tipo=tipo,
            filtros=filtros_dict,
            page=page,
            per_page=10
        )
        return results
    except HTTPException:
        # Re-raise HTTPExceptions from service layer
        raise
    except Exception as e:
        # Log the error with details
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error searching establishments: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": f"An unexpected error occurred while searching establishments: {type(e).__name__}"
            }
        )


@router.get("/get/{cod_unico}/informacion", response_model=EstablishmentInfo)
async def get_establishment_info_endpoint(
    cod_unico: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve complete information about a specific healthcare establishment.
    
    Requirements: 2.1, 2.2, 2.3, 2.4, 6.1, 8.1, 8.2, 8.3
    """
    try:
        establishment_info = await get_establishment_info(db=db, cod_unico=cod_unico)
        return establishment_info
    except HTTPException:
        # Re-raise HTTPExceptions (like 404) from service layer
        raise
    except Exception as e:
        # Log the error (logging will be implemented in task 10)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while retrieving establishment information"
            }
        )
