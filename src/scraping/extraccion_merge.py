import requests
import pandas as pd
import math
import time
import urllib3
import re
import unicodedata

# Desactivamos las alertas de seguridad SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURACIÓN ---
BASE_URL = 'https://app9.susalud.gob.pe:8089/api/renam-consulta/consulta/consultaProgramacion'

# HEADERS (Manteniendo tus credenciales)
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://tua.susalud.gob.pe:8084',
    'Referer': 'https://tua.susalud.gob.pe:8084/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'transfer-encoding-vary-header': 'Vnh4XU9ff0BoaWRGamUAR1MAf0JS', 
}

# --- LISTA DE ESPECIALIDADES (Top Relevantes para Hackaton) ---
# Puedes agregar más IDs de tu lista de 229 si lo necesitas.
ESPECIALIDADES_TOP = {
    "93": "Ginecologia_Obstetricia",
    "121": "Medicina_Familiar",
    "146": "Neumologia",
    "154": "Neurologia",
    "158": "Oftalmologia",
    "168": "Traumatologia",
    "169": "Otorrinolaringologia",
    "177": "Pediatria",
    "181": "Psiquiatria",
    "200": "Urologia",
    "124": "Medicina_Fisica",
    "161": "Oncologia"
}

def limpiar_nombre_archivo(texto):
    """Elimina caracteres especiales para nombres de archivo seguros"""
    nfkd_form = unicodedata.normalize('NFKD', texto)
    texto_sin_tildes = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return re.sub(r'[^a-zA-Z0-9]', '_', texto_sin_tildes).lower()

def extraer_por_especialidad(id_esp, nombre_esp):
    print(f"\n🩺 PROCESANDO: {nombre_esp} (ID: {id_esp})")
    print("="*40)
    
    # Parámetros base para esta iteración
    params = {
        'feInicio': '2025-11-21',
        'feFin': '2025-12-20',
        'profesion': '1',  # Médicos
        'especialidad': id_esp, # ID dinámico
        'nombreIpress': '',
        'nombre': '',
        'paterno': '',
        'materno': '',
        'ubigeo': '15', # Lima
        'size': '10',
        'page': '0'
    }
    
    all_data = []
    
    # 1. OBTENER TOTAL DE PÁGINAS
    try:
        # Reintentos simples en caso de fallo de conexión
        for intento in range(3):
            try:
                response = requests.get(BASE_URL, params=params, headers=headers, verify=False, timeout=10)
                if response.status_code == 200:
                    break
            except:
                time.sleep(2)
        
        data = response.json()
        
        if not data.get("success"):
            print(f"⚠️  La API indicó error para {nombre_esp}: {data.get('message')}")
            return

        total_registros = data["total"]
        if total_registros == 0:
            print(f"⚠️  No hay médicos programados para {nombre_esp} en estas fechas.")
            return

        total_paginas = math.ceil(total_registros / 10)
        print(f"📊 Encontrados: {total_registros} médicos en {total_paginas} páginas.")
        
    except Exception as e:
        print(f"❌ Error conectando inicial para {nombre_esp}: {e}")
        return

    # 2. ITERAR PÁGINAS
    for pagina in range(total_paginas):
        print(f"   ↳ Descargando pág {pagina + 1}/{total_paginas}...", end="\r")
        
        params["page"] = str(pagina)
        
        try:
            resp = requests.get(BASE_URL, params=params, headers=headers, verify=False, timeout=10)
            page_data = resp.json()
            
            if page_data.get("data"):
                all_data.extend(page_data["data"])
            
            time.sleep(0.2) # Pausa corta entre páginas
            
        except Exception as e:
            print(f"\n   ⚠️ Error en pág {pagina}: {e}")

    # 3. GUARDAR CSV
    if all_data:
        df = pd.json_normalize(all_data)
        
        # Nombre dinámico: susalud_cardiologia_lima.csv
        filename = f"susalud_{limpiar_nombre_archivo(nombre_esp)}_lima.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✅ Guardado: {filename} ({len(df)} registros)")
    
    # Pausa larga entre especialidades para evitar bloqueo
    print("\n⏳ Esperando 2 segundos para la siguiente especialidad...")
    time.sleep(2)

def main():
    print("🚀 INICIANDO PIPELINE DE EXTRACCIÓN MASIVA - SUSALUD")
    print(f"🎯 Total de especialidades a procesar: {len(ESPECIALIDADES_TOP)}")
    
    for id_esp, nombre_esp in ESPECIALIDADES_TOP.items():
        extraer_por_especialidad(id_esp, nombre_esp)
        
    print("\n✨✨ PROCESO COMPLETADO EXITOSAMENTE ✨✨")

if __name__ == "__main__":
    main()