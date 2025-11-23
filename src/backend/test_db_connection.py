"""
Script para probar la conexión a la base de datos y consultas básicas.
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.connection import init_db, close_db, get_db_session
from app.db.models import Institucion
from sqlalchemy import select


async def test_connection():
    """Probar conexión y consulta básica."""
    print("=" * 60)
    print("Probando conexión a la base de datos...")
    print("=" * 60)
    
    try:
        # Inicializar conexión
        print("\n1. Inicializando conexión...")
        await init_db()
        print("✅ Conexión inicializada")
        
        # Obtener sesión
        print("\n2. Obteniendo sesión...")
        async for session in get_db_session():
            print("✅ Sesión obtenida")
            
            # Consulta simple
            print("\n3. Ejecutando consulta SELECT...")
            query = select(Institucion).limit(5)
            result = await session.execute(query)
            establishments = result.scalars().all()
            
            print(f"✅ Consulta exitosa. Encontrados {len(establishments)} establecimientos")
            
            # Mostrar algunos datos
            if establishments:
                print("\n4. Primeros establecimientos:")
                for i, est in enumerate(establishments[:3], 1):
                    print(f"   {i}. {est.establecimiento} - {est.direccion}")
            
            break  # Solo necesitamos una iteración
        
        # Cerrar conexión
        print("\n5. Cerrando conexión...")
        await close_db()
        print("✅ Conexión cerrada")
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS PASARON")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_connection())
