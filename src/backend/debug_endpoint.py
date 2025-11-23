"""
Script para debuggear el endpoint /get
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.connection import init_db, close_db, get_db_session
from app.services.establishment_service import search_establishments


async def test_endpoint():
    """Probar el servicio de búsqueda de establecimientos."""
    print("=" * 60)
    print("Probando servicio de búsqueda de establecimientos...")
    print("=" * 60)
    
    try:
        # Inicializar conexión
        print("\n1. Inicializando conexión...")
        await init_db()
        print("✅ Conexión inicializada")
        
        # Obtener sesión y probar búsqueda
        print("\n2. Probando búsqueda sin filtros...")
        async for session in get_db_session():
            try:
                results = await search_establishments(
                    db=session,
                    lugar=None,
                    fecha=None,
                    tipo=None,
                    filtros=None
                )
                
                print(f"✅ Búsqueda exitosa. Encontrados {len(results)} establecimientos")
                
                # Mostrar algunos resultados
                if results:
                    print("\n3. Primeros resultados:")
                    for i, est in enumerate(results[:3], 1):
                        print(f"   {i}. {est.nombre}")
                        print(f"      Dirección: {est.direccion}")
                        print(f"      Código: {est.cod_unico}")
                        print()
                else:
                    print("⚠️  No se encontraron establecimientos")
                
            except Exception as e:
                print(f"\n❌ ERROR en búsqueda: {type(e).__name__}: {str(e)}")
                import traceback
                traceback.print_exc()
            
            break  # Solo necesitamos una iteración
        
        # Cerrar conexión
        print("\n4. Cerrando conexión...")
        await close_db()
        print("✅ Conexión cerrada")
        
        print("\n" + "=" * 60)
        print("✅ PRUEBA COMPLETADA")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_endpoint())
