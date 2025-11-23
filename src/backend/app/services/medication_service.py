"""Medication service for healthcare API."""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.db.models import MedicInst, Medicamentos, Institucion
from app.schemas.responses import MedicationInfo


async def search_medications(
    db: AsyncSession,
    cod_unico: str,
    filtros: Optional[Dict[str, Any]] = None
) -> List[MedicationInfo]:
    """
    Search for available medications at a specific establishment with filtering.
    
    Queries MedicInst table by cod_unico, joins with Medicamentos table for
    complete information, applies filters (name, type, pharmaceutical form,
    availability), excludes zero-stock medications by default, includes
    zero-stock if explicitly requested in filters, and returns list of
    MedicationInfo objects.
    
    Args:
        db: Database session
        cod_unico: Unique establishment identifier
        filtros: Optional filters (nombre, tipo, forma_farmaceutica, 
                 disponibilidad, incluir_sin_stock)
        
    Returns:
        List of MedicationInfo objects
        
    Requirements: 5.1, 5.2, 5.3, 5.4
    """
    # Start with base query joining MedicInst and Medicamentos
    query = (
        select(MedicInst)
        .options(selectinload(MedicInst.medicamento_rel))
        .filter(MedicInst.cod_unico == cod_unico)
    )
    
    # Execute query
    result = await db.execute(query)
    medic_inst_records = result.scalars().all()
    
    # Apply filters and build response
    medications = []
    
    for record in medic_inst_records:
        medicamento = record.medicamento_rel
        
        # Skip if medicamento relationship is not loaded
        if not medicamento:
            continue
        
        # Apply filters if provided
        if filtros:
            # Filter by medication name (case-insensitive partial match)
            if 'nombre' in filtros and filtros['nombre']:
                if filtros['nombre'].lower() not in medicamento.nombre_med.lower():
                    continue
            
            # Filter by medication type
            if 'tipo' in filtros and filtros['tipo']:
                if medicamento.tipomed != filtros['tipo']:
                    continue
            
            # Filter by pharmaceutical form
            if 'forma_farmaceutica' in filtros and filtros['forma_farmaceutica']:
                if medicamento.formaf != filtros['forma_farmaceutica']:
                    continue
            
            # Filter by availability indicator
            if 'disponibilidad' in filtros and filtros['disponibilidad'] is not None:
                # Assuming indicador field represents availability
                # True means available, False means not available
                is_available = record.indicador and record.indicador.lower() in ['si', 'yes', 'disponible', '1', 'true']
                if filtros['disponibilidad'] != is_available:
                    continue
        
        # Exclude zero-stock medications by default
        # Include them only if explicitly requested
        incluir_sin_stock = filtros.get('incluir_sin_stock', False) if filtros else False
        if record.stock_tot == 0 and not incluir_sin_stock:
            continue
        
        # Build MedicationInfo object
        medications.append(
            MedicationInfo(
                codigo_med=medicamento.codigo_med,
                nombre=medicamento.nombre_med,
                forma_farmaceutica=medicamento.formaf,
                tipo=medicamento.tipomed,
                stock=record.stock_tot,
                precio=record.precio,
                fecha_vencimiento=record.fecha_venc,
                disponible=record.indicador
            )
        )
    
    return medications



async def search_medicine_by_name(
    db: AsyncSession,
    nombre: str
) -> List[Dict[str, Any]]:
    """
    Search for medicines by name across all establishments.
    
    Returns medicine information with establishments where it's available and stock.
    
    Args:
        db: Database session
        nombre: Medicine name to search for (partial match)
        
    Returns:
        List of dictionaries with medicine and establishment information
    """
    # Query for medicines matching the name
    query = (
        select(Medicamentos, MedicInst, Institucion)
        .join(MedicInst, Medicamentos.codigo_med == MedicInst.codigo_med)
        .join(Institucion, MedicInst.cod_unico == Institucion.cod_unico)
        .filter(Medicamentos.nombre_med.ilike(f"%{nombre}%"))
        .filter(MedicInst.stock_tot > 0)  # Only show medicines with stock
    )
    
    result = await db.execute(query)
    records = result.all()
    
    # Group by medicine
    medicines_dict = {}
    
    for medicamento, medic_inst, institucion in records:
        med_key = medicamento.codigo_med
        
        if med_key not in medicines_dict:
            medicines_dict[med_key] = {
                "codigo_med": medicamento.codigo_med,
                "nombre": medicamento.nombre_med,
                "forma_farmaceutica": medicamento.formaf,
                "tipo": medicamento.tipomed,
                "establecimientos": []
            }
        
        # Add establishment information
        medicines_dict[med_key]["establecimientos"].append({
            "cod_unico": institucion.cod_unico,
            "nombre": institucion.establecimiento,
            "direccion": institucion.direccion,
            "stock": medic_inst.stock_tot,
            "precio": float(medic_inst.precio) if medic_inst.precio else 0.0,
            "fecha_vencimiento": medic_inst.fecha_venc.isoformat() if medic_inst.fecha_venc else None,
            "disponible": medic_inst.indicador
        })
    
    # Convert to list and sort establishments by stock (descending)
    result_list = []
    for medicine in medicines_dict.values():
        medicine["establecimientos"].sort(key=lambda x: x["stock"], reverse=True)
        result_list.append(medicine)
    
    # Sort medicines by name
    result_list.sort(key=lambda x: x["nombre"])
    
    return result_list
