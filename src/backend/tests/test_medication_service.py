"""Property-based tests for medication service."""

import pytest
from hypothesis import given, strategies as st, settings
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta

from app.services.medication_service import search_medications
from app.db.models import MedicInst, Medicamentos


# Strategy for generating medication data
@st.composite
def medication_data_strategy(draw):
    """Generate valid medication data for testing."""
    codigo_med = draw(st.text(min_size=5, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))))
    nombre_med = draw(st.text(min_size=3, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))))
    formaf = draw(st.text(min_size=3, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))))
    tipomed = draw(st.text(min_size=3, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))))
    stock_tot = draw(st.integers(min_value=0, max_value=1000))
    precio = draw(st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False))
    indicador = draw(st.sampled_from(['Si', 'No', 'Disponible', 'No disponible']))
    
    # Generate a date within the next 2 years
    days_ahead = draw(st.integers(min_value=1, max_value=730))
    fecha_venc = date.today() + timedelta(days=days_ahead)
    
    return {
        'codigo_med': codigo_med,
        'nombre_med': nombre_med,
        'formaf': formaf,
        'tipomed': tipomed,
        'stock_tot': stock_tot,
        'precio': precio,
        'indicador': indicador,
        'fecha_venc': fecha_venc
    }


# Feature: healthcare-api, Property 12: Zero-stock exclusion
@given(
    cod_unico=st.text(min_size=5, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    medications=st.lists(medication_data_strategy(), min_size=1, max_size=20),
    incluir_sin_stock=st.booleans()
)
@settings(max_examples=100)
@pytest.mark.asyncio
async def test_zero_stock_exclusion(cod_unico, medications, incluir_sin_stock):
    """
    Property 12: Zero-stock exclusion
    
    For any medication search without explicit stock filters, medications with 
    zero stock should be excluded from results, but when explicitly requested 
    in filters, zero-stock medications should be included.
    
    Validates: Requirements 5.4
    """
    # Create mock database session
    mock_db = AsyncMock(spec=AsyncSession)
    
    # Create mock MedicInst and Medicamentos objects
    mock_records = []
    zero_stock_count = 0
    non_zero_stock_count = 0
    
    for med_data in medications:
        # Create mock Medicamentos object
        mock_medicamento = MagicMock(spec=Medicamentos)
        mock_medicamento.codigo_med = med_data['codigo_med']
        mock_medicamento.nombre_med = med_data['nombre_med']
        mock_medicamento.formaf = med_data['formaf']
        mock_medicamento.tipomed = med_data['tipomed']
        
        # Create mock MedicInst object
        mock_medic_inst = MagicMock(spec=MedicInst)
        mock_medic_inst.cod_unico = cod_unico
        mock_medic_inst.codigo_med = med_data['codigo_med']
        mock_medic_inst.stock_tot = med_data['stock_tot']
        mock_medic_inst.precio = med_data['precio']
        mock_medic_inst.indicador = med_data['indicador']
        mock_medic_inst.fecha_venc = med_data['fecha_venc']
        mock_medic_inst.medicamento_rel = mock_medicamento
        
        mock_records.append(mock_medic_inst)
        
        # Count zero and non-zero stock medications
        if med_data['stock_tot'] == 0:
            zero_stock_count += 1
        else:
            non_zero_stock_count += 1
    
    # Mock the query result
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = mock_records
    mock_db.execute.return_value = mock_result
    
    # Call the medication service with or without incluir_sin_stock filter
    filtros = {'incluir_sin_stock': incluir_sin_stock} if incluir_sin_stock else {}
    results = await search_medications(
        db=mock_db,
        cod_unico=cod_unico,
        filtros=filtros
    )
    
    # Verify zero-stock exclusion behavior
    if incluir_sin_stock:
        # When incluir_sin_stock is True, all medications should be included
        assert len(results) == len(medications), \
            f"With incluir_sin_stock=True, expected {len(medications)} medications, got {len(results)}"
        
        # Verify that zero-stock medications are included
        zero_stock_in_results = sum(1 for med in results if med.stock == 0)
        assert zero_stock_in_results == zero_stock_count, \
            f"Expected {zero_stock_count} zero-stock medications in results, got {zero_stock_in_results}"
    else:
        # When incluir_sin_stock is False or not provided, zero-stock should be excluded
        assert len(results) == non_zero_stock_count, \
            f"Without incluir_sin_stock, expected {non_zero_stock_count} medications, got {len(results)}"
        
        # Verify that no zero-stock medications are in results
        for med in results:
            assert med.stock > 0, \
                f"Found zero-stock medication in results when incluir_sin_stock=False: {med.nombre}"
