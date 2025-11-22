import pandas as pd
import glob
import os

def unir_csvs():
    print("🚀 INICIANDO PROCESO DE UNIFICACIÓN DE DATOS (MODO TEXTO ESTRICTO)")
    
    # 1. Buscar todos los archivos CSV en la carpeta actual
    archivos_csv = glob.glob("susalud_*.csv")
    
    if not archivos_csv:
        print("❌ No se encontraron archivos CSV que empiecen con 'susalud_' en esta carpeta.")
        return

    print(f"📂 Se encontraron {len(archivos_csv)} archivos para procesar.")
    
    lista_dataframes = []
    
    # 2. Leer y acumular cada archivo
    for archivo in archivos_csv:
        try:
            # CRUCIAL: dtype=str fuerza a que TODO sea texto.
            # keep_default_na=False evita que vacíos se conviertan en NaN (flotantes)
            df_temp = pd.read_csv(archivo, dtype=str, keep_default_na=False)
            
            # Opcional: Agregar una columna para saber de qué archivo vino
            df_temp["source_file"] = archivo
            
            lista_dataframes.append(df_temp)
            
        except Exception as e:
            print(f"   ⚠️ Error leyendo {archivo}: {e}")

    if not lista_dataframes:
        print("❌ No se pudo leer ningún DataFrame válido.")
        return

    # 3. Concatenar (Unir todo)
    print("\n🔄 Uniendo archivos...")
    df_maestro = pd.concat(lista_dataframes, ignore_index=True, sort=False)
    
    print(f"📊 Total de registros brutos: {len(df_maestro)}")


    # 6. Guardar el Archivo Maestro
    nombre_final = "SUSALUD_MASTER_DATA_LIMA.csv"
    
    # Guardamos sin index y forzando utf-8 con BOM (sig) para que Excel abra bien las tildes
    df_maestro.to_csv(nombre_final, index=False, encoding='utf-8-sig')
    
    print("\n" + "="*50)
    print(f"✅ ¡ÉXITO! Archivo maestro creado: {nombre_final}")
    print(f"📈 Total final de registros únicos: {len(df_maestro)}")
    print(f"📝 Tipos de datos asegurados como Texto (Strings)")
    print("="*50)

if __name__ == "__main__":
    unir_csvs()