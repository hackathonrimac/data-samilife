from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# --- Output Schemas ---

class InstitucionResultado(BaseModel):
    nombre: str
    direccion: str
    calificacion: float

class CitaDisponible(BaseModel):
    # Estructura flexible ya que es shapeless en el retorno
    info: Dict[str, Any]

class PrecioServicio(BaseModel):
    precio_normal: int # O float, según prefieras
    precio_rimac: int

class FarmacoInfo(BaseModel):
    nombre: str
    precio: float
    stock: int
    detalles: Dict[str, Any]