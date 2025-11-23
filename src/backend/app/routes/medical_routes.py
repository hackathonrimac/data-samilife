from fastapi import APIRouter, Query, Body, Path
from typing import List, Dict, Any
from app.schemas import schemas

router = APIRouter()

# --- Mock Data (Datos falsos para prueba) ---
MOCK_INSTITUCIONES = [
    {"nombre": "Clínica San Felipe", "direccion": "Av. Gregorio Escobedo 650", "calificacion": 4.8},
    {"nombre": "Clínica Ricardo Palma", "direccion": "Av. Javier Prado Este 1066", "calificacion": 4.5},
    {"nombre": "Hospital Santa Rosa", "direccion": "Av. Bolívar S/N", "calificacion": 3.9},
]

# --- Endpoints ---

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/get", response_model=List[schemas.InstitucionResultado])
async def get_establecimientos(
    lugar: str = Query(..., description="Distrito o ciudad"),
    fecha: str = Query(..., description="Fecha deseada YYYY-MM-DD"),
    tipo: str = Query(..., description="Tipo de establecimiento"),
    filtros: Dict[str, Any] = Body({}, description="Filtros adicionales (shapeless)")
):
    """
    Devuelve una lista estática de establecimientos simulados.
    Ignora los filtros de entrada por ahora.
    """
    return MOCK_INSTITUCIONES


@router.get("/get/{codigo}/informacion", response_model=Dict[str, Any])
async def get_info(
    codigo: str = Path(..., description="Código del establecimiento")
):
    """
    Devuelve información detallada simulada de un establecimiento específico.
    """
    return {
        "cod_inst": codigo,
        "nombre": "Clínica San Felipe",
        "ruc": "20100038591",
        "telefono": "219-0000",
        "horario_atencion": "24 Horas",
        "especialidades": ["Cardiología", "Pediatría", "Traumatología"]
    }


@router.post("/get/{codigo}/citas", response_model=List[Dict[str, Any]])
async def get_citas(
    codigo: str = Path(...), 
    filtros: Dict[str, Any] = Body(...)
):
    """
    Devuelve una lista simulada de citas disponibles.
    """
    return [
        {
            "id_cita": "C-001",
            "fecha": "2023-11-25",
            "hora": "09:00",
            "especialidad": "Cardiología",
            "doctor": "Dr. Juan Pérez",
            "consultorio": "305"
        },
        {
            "id_cita": "C-002",
            "fecha": "2023-11-25",
            "hora": "10:30",
            "especialidad": "Cardiología",
            "doctor": "Dra. Maria Lopez",
            "consultorio": "306"
        }
    ]


@router.post("/get/precio/cita", response_model=schemas.PrecioServicio)
async def get_precio(
    codigo: str = Query(...), 
    servicio: Dict[str, Any] = Body(...)
):
    """
    Devuelve precios simulados (Regular vs Rimac).
    """
    # Simulamos que el servicio cuesta 200 y con Rimac baja a 80
    return schemas.PrecioServicio(
        precio_normal=200,
        precio_rimac=80
    )


@router.post("/get/{codigo}/farmacos", response_model=List[Dict[str, Any]])
async def get_farmacos(
    codigo: str = Path(...),
    filtros: Dict[str, Any] = Body(...)
):
    """
    Devuelve una lista simulada de fármacos disponibles en ese establecimiento.
    """
    return [
        {
            "cod_med": "M-101",
            "nombre": "Paracetamol 500mg",
            "marca": "Generico",
            "precio_unidad": 1.50,
            "stock": 100
        },
        {
            "cod_med": "M-102",
            "nombre": "Ibuprofeno 400mg",
            "marca": "Doloral",
            "precio_unidad": 3.80,
            "stock": 45
        }
    ]