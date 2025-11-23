"""Request schemas for API endpoints."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import date


class EstablishmentSearchParams(BaseModel):
    """Parameters for searching healthcare establishments.
    
    Validates: Requirements 1.1, 1.2, 1.3, 1.4
    """
    lugar: Optional[str] = Field(None, description="Location/address to filter by")
    fecha: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    tipo: Optional[str] = Field(None, description="Institution type (público/privado)")
    filtros: Optional[Dict[str, Any]] = Field(None, description="Custom JSON filters")
    
    @field_validator('fecha')
    @classmethod
    def validate_fecha(cls, v: Optional[str]) -> Optional[str]:
        """Validate date format is YYYY-MM-DD."""
        if v is None:
            return v
        try:
            # Try parsing to validate format
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


class AppointmentFilters(BaseModel):
    """Filters for appointment search.
    
    Validates: Requirements 3.2
    """
    especialidad: Optional[str] = Field(None, description="Medical specialty")
    profesional: Optional[str] = Field(None, description="Professional name or CMP")
    fecha_inicio: Optional[str] = Field(None, description="Start date for range (YYYY-MM-DD)")
    fecha_fin: Optional[str] = Field(None, description="End date for range (YYYY-MM-DD)")
    tipo_servicio: Optional[str] = Field(None, description="Type of service")
    
    @field_validator('fecha_inicio', 'fecha_fin')
    @classmethod
    def validate_dates(cls, v: Optional[str]) -> Optional[str]:
        """Validate date format is YYYY-MM-DD."""
        if v is None:
            return v
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


class MedicationFilters(BaseModel):
    """Filters for medication search.
    
    Validates: Requirements 5.2
    """
    nombre: Optional[str] = Field(None, description="Medication name")
    tipo: Optional[str] = Field(None, description="Medication type")
    forma_farmaceutica: Optional[str] = Field(None, description="Pharmaceutical form")
    disponibilidad: Optional[bool] = Field(None, description="Availability status")
    incluir_sin_stock: Optional[bool] = Field(False, description="Include zero-stock medications")


class ServiceDetails(BaseModel):
    """Service details for pricing requests.
    
    Validates: Requirements 4.1
    """
    codigo: str = Field(..., description="Establishment unique code (cod_unico)")
    servicio: str = Field(..., description="Service name or type")
    cmp: Optional[str] = Field(None, description="Professional CMP code")
    profesion: Optional[str] = Field(None, description="Professional type")
