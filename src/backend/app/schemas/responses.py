"""Response schemas for API endpoints."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import date


class EstablishmentSummary(BaseModel):
    """Summary information for establishment search results.
    
    Validates: Requirements 1.5
    """
    nombre: str = Field(..., description="Establishment name")
    direccion: str = Field(..., description="Establishment address")
    calificacion: Optional[str] = Field(None, description="Establishment rating/classification")
    cod_unico: Optional[str] = Field(None, description="Unique establishment code")
    latitud: Optional[float] = Field(None, description="Latitude coordinate")
    longitud: Optional[float] = Field(None, description="Longitude coordinate")
    
    class Config:
        from_attributes = True  # Permite crear desde objetos ORM


class ServiceInfo(BaseModel):
    """Information about a service offered at an establishment."""
    servicio: str = Field(..., description="Service name/type")
    profesional: Optional[str] = Field(None, description="Professional name")
    especialidad: Optional[str] = Field(None, description="Medical specialty")
    telefono: Optional[str] = Field(None, description="Contact phone")


class ProfessionalInfo(BaseModel):
    """Information about a healthcare professional."""
    cmp: str = Field(..., description="Professional registration code")
    nombre: str = Field(..., description="Professional name")
    profesion: str = Field(..., description="Professional type")
    especialidad: Optional[str] = Field(None, description="Medical specialty")


class InsuranceInfo(BaseModel):
    """Insurance coverage information."""
    seguro: str = Field(..., description="Insurance provider name")
    red: Optional[str] = Field(None, description="Insurance network")
    costo_consulta: Optional[float] = Field(None, description="Consultation cost with insurance")


class EstablishmentInfo(BaseModel):
    """Complete establishment information.
    
    Validates: Requirements 2.1, 2.4
    """
    cod_unico: str = Field(..., description="Unique establishment code")
    nombre: str = Field(..., description="Establishment name")
    direccion: str = Field(..., description="Address")
    institucion: str = Field(..., description="Institution type (público/privado)")
    establecimiento: str = Field(..., description="Establishment type")
    clasificacion: str = Field(..., description="Classification")
    correo: Optional[str] = Field(None, description="Email address")
    longitud: Optional[float] = Field(None, description="Longitude coordinate")
    latitud: Optional[float] = Field(None, description="Latitude coordinate")
    pagina: Optional[str] = Field(None, description="Website URL")
    servicios: List[ServiceInfo] = Field(default_factory=list, description="Available services")
    profesionales: List[ProfessionalInfo] = Field(default_factory=list, description="Healthcare professionals")
    seguros: List[InsuranceInfo] = Field(default_factory=list, description="Accepted insurance providers")


class ScheduleEntry(BaseModel):
    """Schedule entry for an appointment slot."""
    dia: int = Field(..., description="Day of month")
    ini: str = Field(..., description="Start datetime")
    fin: str = Field(..., description="End datetime")


class AppointmentSlot(BaseModel):
    """Available appointment slot information.
    
    Validates: Requirements 3.5
    """
    profesional: str = Field(..., description="Professional name")
    cmp: Optional[str] = Field(None, description="Professional CMP code")
    especialidad: Optional[str] = Field(None, description="Medical specialty")
    servicio: str = Field(..., description="Service type")
    horario: List[ScheduleEntry] = Field(..., description="Schedule details")
    telefono: Optional[str] = Field(None, description="Contact phone number")


class PricingInfo(BaseModel):
    """Service pricing information.
    
    Validates: Requirements 4.5
    """
    precio_normal: int = Field(..., description="Regular price without insurance")
    precio_rimac: int = Field(..., description="Price with Rimac insurance")


class MedicationInfo(BaseModel):
    """Medication details with availability.
    
    Validates: Requirements 5.3
    """
    codigo_med: str = Field(..., description="Medication code")
    nombre: str = Field(..., description="Medication name")
    forma_farmaceutica: str = Field(..., description="Pharmaceutical form")
    tipo: str = Field(..., description="Medication type")
    stock: int = Field(..., description="Available stock quantity")
    precio: float = Field(..., description="Price")
    fecha_vencimiento: Optional[date] = Field(None, description="Expiration date")
    disponible: str = Field(..., description="Availability indicator")


class ErrorDetail(BaseModel):
    """Detailed error information."""
    field: Optional[str] = Field(None, description="Field that caused the error")
    message: str = Field(..., description="Error message")
    expected: Optional[str] = Field(None, description="Expected value or format")
    received: Optional[str] = Field(None, description="Received value")


class ErrorResponse(BaseModel):
    """Standardized error response format.
    
    Validates: Requirements 8.5
    """
    error: Dict[str, Any] = Field(..., description="Error information")
    
    @classmethod
    def create(cls, code: str, message: str, details: Optional[Dict[str, Any]] = None) -> "ErrorResponse":
        """Create a standardized error response."""
        error_data = {
            "code": code,
            "message": message
        }
        if details:
            error_data["details"] = details
        return cls(error=error_data)
