"""Property-based tests for pricing service."""

import pytest
from hypothesis import given, strategies as st, settings
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.pricing_service import get_service_pricing
from app.schemas.responses import PricingInfo
from app.db.models import Servicio, Asegurado


# Strategy for generating service data
@st.composite
def service_data_strategy(draw):
    """Generate valid service data for testing."""
    codigo = draw(st.text(min_size=5, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))))
    servicio = draw(st.text(min_size=3, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs'))))
    cmp = draw(st.text(min_size=5, max_size=15, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))))
    profesion = draw(st.text(min_size=3, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))))
    
    return {
        'codigo': codigo,
        'servicio': servicio,
        'cmp': cmp,
        'profesion': profesion
    }


# Feature: healthcare-api, Property 9: No-insurance pricing equality
@given(service_data_strategy())
@settings(max_examples=100)
@pytest.mark.asyncio
async def test_no_insurance_pricing_equality(service_data):
    """
    Property 9: No-insurance pricing equality
    
    For any establishment without insurance coverage, the regular price 
    and insured price should be equal.
    
    Validates: Requirements 4.3
    """
    # Create mock database session
    mock_db = AsyncMock(spec=AsyncSession)
    
    # Create mock service object
    mock_service = MagicMock(spec=Servicio)
    mock_service.cod_unico = service_data['codigo']
    mock_service.servicio = service_data['servicio']
    mock_service.cmp = service_data['cmp']
    mock_service.profesion = service_data['profesion']
    
    # Mock the service query to return the service
    service_result = MagicMock()
    service_result.scalar_one_or_none.return_value = mock_service
    
    # Mock the insurance query to return None (no insurance coverage)
    insurance_result = MagicMock()
    insurance_result.scalar_one_or_none.return_value = None
    
    # Configure mock_db.execute to return different results for different queries
    mock_db.execute.side_effect = [service_result, insurance_result]
    
    # Call the pricing service
    pricing = await get_service_pricing(
        db=mock_db,
        codigo=service_data['codigo'],
        servicio=service_data['servicio'],
        cmp=service_data['cmp'],
        profesion=service_data['profesion']
    )
    
    # Verify that both prices are equal when no insurance is available
    assert pricing.precio_normal == pricing.precio_rimac, \
        f"Without insurance coverage, precio_normal ({pricing.precio_normal}) should equal precio_rimac ({pricing.precio_rimac})"
    
    # Verify that both prices are integers
    assert isinstance(pricing.precio_normal, int), \
        f"precio_normal should be an integer, got {type(pricing.precio_normal)}"
    assert isinstance(pricing.precio_rimac, int), \
        f"precio_rimac should be an integer, got {type(pricing.precio_rimac)}"
