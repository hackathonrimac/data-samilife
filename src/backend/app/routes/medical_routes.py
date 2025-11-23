from fastapi import APIRouter, Depends, Query, Body
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.db.database import get_db # Asumiendo que tienes una funcion get_db
from app.services import medical_service
from app.schemas import schemas

router = APIRouter()

@router.post("/get", response_model=List[schemas.InstitucionResultado])
def get_establecimientos(
    lugar: str = Query(...),
    fecha: str = Query(...),
    tipo: str = Query(...),
    filtros: Dict[str, Any] = Body(...), # JSON shapeless viene en el body
    db: Session = Depends(get_db)
):
    return medical_service.buscar_establecimientos(db, lugar, fecha, tipo, filtros)

@router.get("/get/{codigo}/informacion", response_model=Dict[str, Any])
def get_info(codigo: str, db: Session = Depends(get_db)):
    return medical_service.obtener_info_establecimiento(db, codigo)

@router.post("/get/{codigo}/citas", response_model=List[Dict[str, Any]])
def get_citas(
    codigo: str, 
    filtros: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    return medical_service.buscar_citas(db, codigo, filtros)

@router.post("/get/precio/cita", response_model=schemas.PrecioServicio)
def get_precio(
    codigo: str = Query(...), # El parámetro dice 'codigo', asumo query param o path
    servicio: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    return medical_service.calcular_precios(db, codigo, servicio)

@router.post("/get/{codigo}/farmacos", response_model=List[Dict[str, Any]])
def get_farmacos(
    codigo: str,
    filtros: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    return medical_service.buscar_farmacos(db, codigo, filtros)