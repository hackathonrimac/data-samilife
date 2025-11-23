"""Appointment routes for healthcare API."""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.db.connection import get_db_session
from app.services.appointment_service import get_available_appointments
from app.schemas.responses import AppointmentSlot

router = APIRouter(prefix="", tags=["appointments"])


@router.get("/get/{cod_unico}/citas", response_model=List[AppointmentSlot])
async def get_appointments_endpoint(
    cod_unico: str,
    filtros: Optional[str] = Query(None, description="JSON filters for appointments"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get available appointment slots at a specific establishment with filtering.
    
    Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 6.1
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
        appointments = await get_available_appointments(
            db=db,
            cod_unico=cod_unico,
            filtros=filtros_dict
        )
        return appointments
    except Exception as e:
        # Log the error (logging will be implemented in task 10)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while retrieving appointments"
            }
        )
