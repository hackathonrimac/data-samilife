import requests
import pandas as pd
import math
import time
import urllib3
import re
import unicodedata
import argparse
from typing import Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://app9.susalud.gob.pe:8089/api/renam-consulta/consulta/consultaProgramacion'

DEFAULT_HEADERS = {
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
    'sec-ch-ua-platform': '"Windows"'
}

HEADERS_ODONTO = {
    **DEFAULT_HEADERS,
    'transfer-encoding-vary-header': 'Vnh4XU9ff0BoaWRGamUAR1MAf0JS'
}

HEADERS_PSICO = {
    **DEFAULT_HEADERS,
    'transfer-encoding-vary-header': 'Vnh4XU9ff0BoaWRGamUAR1MAf0JS'
}

PROFESION_MAP = {
    'medicos': '1',
    'odontologos': '3',
    'psicologos': '6',
    'nutricionistas': '8'
}

COOKIES_MAP = {
    'medicos': None,
    'odontologos': None,
    'psicologos': {'ar_debug': '1'},
    'nutricionistas': None
}

HEADERS_MAP = {
    'medicos': DEFAULT_HEADERS,
    'odontologos': HEADERS_ODONTO,
    'psicologos': HEADERS_PSICO,
    'nutricionistas': DEFAULT_HEADERS
}

ESPECIALIDADES_MAP = {
    'odontologos': {
        "": "ODONTOLOGOS GENERALES / SIN ESPECIALIDAD",
        "214": "ADMINISTRACIÓN Y GESTIÓN EN ESTOMATOLOGÍA",
        "215": "AUDITORIA ODONTOLÓGICA",
        "216": "CIRUGÍA BUCAL Y MAXILOFACIAL",
        "217": "ENDODONCIA",
        "218": "ESTOMATOLOGÍA DE PACIENTES ESPECIALES",
        "497": "IMPLANTOLOGIA",
        "219": "MEDICINA Y PATOLOGÍA ESTOMATOLÓGICA",
        "220": "ODONTOGERIATRÍA",
        "221": "ODONTOLOGÍA FORENSE",
        "222": "ODONTOLOGÍA RESTAURADORA Y ESTÉTICA",
        "223": "ODONTOPEDIATRÍA",
        "224": "ORTODONCIA Y ORTOPEDIA MAXILAR",
        "225": "PERIODONCIA E IMPLANTOLOGÍA",
        "226": "RADIOLOGÍA BUCAL Y MAXILOFACIAL",
        "227": "REHABILITACIÓN ORAL",
        "228": "SALUD FAMILIAR Y COMUNITARIA EN ODONTOLOGÍA",
        "229": "SALUD PÚBLICA ESTOMATOLÓGICA"
    },
    'nutricionistas': {
        "": "NUTRICIONISTAS SIN ESPECIALIDAD (GENERAL)",
        "492": "NUTRICION CLINICA CON MENCION EN NUTRICION ONCOLOGICA",
        "363": "NUTRICIÓN DEPORTIVA",
        "463": "NUTRICIÓN ONCOLÓGICA",
        "362": "NUTRICIÓN PÚBLICA"
    },
    'psicologos': {
        "": "PSICOLOGOS GENERALES / SIN ESPECIALIDAD",
        "499": "NEUROPSICOLOGÍA",
        "498": "NEUROPSICOLOGÍA INFANTIL Y APRENDIZAJE",
        "343": "PSICOLOGÍA CLÍNICA Y DE LA SALUD",
        "344": "PSICOLOGÍA DE LA FAMILIA",
        "345": "PSICOLOGÍA DE LAS ADICCIONES",
        "346": "PSICOLOGÍA DE LAS EMERGENCIAS Y DESASTRES",
        "347": "PSICOLOGÍA DEL ADULTO MAYOR",
        "348": "PSICOLOGÍA DEL DEPORTE",
        "349": "PSICOLOGÍA EDUCACIONAL",
        "350": "PSICOLOGÍA JURÍDICA",
        "351": "PSICOLOGÍA ORGANIZACIONAL",
        "352": "PSICOLOGÍA PENITENCIARIA",
        "353": "PSICOLOGÍA POLICIAL-MILITAR",
        "354": "PSICOLOGÍA SOCIAL-COMUNITARIA"
    },
    'medicos': {
        "1": "ADMINISTRACION DE HOSPITALES",
        "2": "ADMINISTRACION DE SALUD",
        "3": "ADMINISTRACION Y GESTION EN SALUD",
        "4": "ADOLESCENTOLOGIA",
        "5": "ALERGIA E INMULOGIA CLINICA PEDIATRICA",
        "410": "ALERGIA E INMUNOLOGIA CLINICA PEDIATRA",
        "6": "ALERGIA E INMUNOPATOLOGIA",
        "424": "ALERGIAS E INMUNOLOGÍA",
        "7": "ALERGOLOGIA",
        "8": "ANALISIS CLINICOS",
        "9": "ANATOMIA HUMANA",
        "10": "ANATOMIA PATOLOGICA",
        "11": "ANATOMIA PATOLOGICA - PATOLOGIA CLINICA",
        "12": "ANATOMIA PATOLOGICA Y LABORATORIO",
        "412": "ANATOMIA PATOLOGICA-PATOLOGIA CLINICA",
        "13": "ANESTESIA, ANALGESIA Y REANIMACION",
        "14": "ANESTESIOLOGIA",
        "15": "ANESTESIOLOGIA CARDIOVASCULAR",
        "16": "ANESTESIOLOGIA OBSTETRICA",
        "17": "ANESTESIOLOGIA Y CUIDADOS INTENSIVOS",
        "18": "ANESTESIOLOGIA Y REANIMACION",
        "19": "ANESTESIOLOGIA Y TERAPIA INTENSIVA CARDIOVASCULAR",
        "20": "ANGIOLOGIA",
        "21": "APARATO DIGESTIVO",
        "22": "ARTROSCOPIA Y CIRUGIA DE RODILLA",
        "431": "CARDIO INTERVENCIONISTA",
        "24": "CARDIOLOGIA",
        "25": "CARDIOLOGIA INFANTIL",
        "427": "CARDIOLOGIA PEDIATRICA",
        "26": "CIRUGIA",
        "27": "CIRUGIA CARDIOVASCULAR",
        "28": "CIRUGIA CARDIOVASCULAR PEDIATRICA",
        "29": "CIRUGIA COLORRECTAL",
        "30": "CIRUGIA CRANEOMAXILOFACIAL",
        "413": "CIRUGIA DE CABEZA, CUELLO Y MAXILO FACIAL",
        "32": "CIRUGIA DE CABEZA, CUELLO Y MAXILOFACIAL",
        "31": "CIRUGIA DE CABEZA Y CUELLO",
        "33": "CIRUGIA DE LA RODILLA",
        "34": "CIRUGIA DE MANO",
        "35": "CIRUGIA DE TORAX",
        "36": "CIRUGIA DEL APARATO DIGESTIVO",
        "37": "CIRUGIA ENDOSCOPICA GINECOLOGICA",
        "38": "CIRUGIA GASTROENTEROLOGICA",
        "39": "CIRUGIA GENERAL",
        "425": "CIRUGIA GENERAL Y LAPAROSCOPICA",
        "40": "CIRUGIA GENERAL Y ONCOLOGICA",
        "41": "CIRUGIA HEPATOPANCREATOBILIAR Y TRANSPLANTE",
        "42": "CIRUGIA HOSPITALARIA",
        "43": "CIRUGIA NEUMOLOGICA",
        "44": "CIRUGIA ONCOLOGICA",
        "45": "CIRUGIA ONCOLOGICA ABDOMINAL",
        "46": "CIRUGIA ONCOLOGICA DE CABEZA Y CUELLO",
        "449": "CIRUGIA ONCOLÓGICA DE MAMAS",
        "47": "CIRUGIA ONCOLOGICA DE MAMAS, TEJIDOS BLANDOS Y PIEL",
        "448": "CIRUGIA ONCOLÓGICA DE TORAX",
        "414": "CIRUGIA ONCOLOGICA E CABEZA Y CUELLO",
        "48": "CIRUGIA ORTOPEDICA Y TRAUMATOLOGIA",
        "49": "CIRUGIA PEDIATRICA",
        "50": "CIRUGIA PLASTICA",
        "51": "CIRUGIA PLASTICA FACIAL",
        "57": "CIRUGIA PLASTICA, RECONSTRUCTIVA, ESTETICA Y MAXILO FACIAL",
        "56": "CIRUGIA PLASTICA, RECONSTRUCTIVA Y ESTETICA",
        "52": "CIRUGIA PLASTICA Y CAUMATOLOGIA",
        "53": "CIRUGIA PLASTICA Y RECONSTRUCTIVA",
        "54": "CIRUGIA PLASTICA Y REPARADORA",
        "55": "CIRUGIA PLASTICA Y REPARADORA DE MANO",
        "58": "CIRUGIA TORACICA Y CARDIOVASCULAR",
        "62": "CIRUGIA, TRANSPLANTOLOGIA Y ANDROLOGIA",
        "450": "CIRUGIA UNIDAD PISO PÉLVICO",
        "59": "CIRUGIA VASCULAR",
        "60": "CIRUGIA VASCULAR PERIFERICA",
        "61": "CIRUGIA VASCULAR Y ANGIOLOGIA",
        "63": "COLOPROCTOLOGIA",
        "64": "DERMATOLOGIA",
        "65": "DERMATOLOGIA PEDIATRICA",
        "66": "DERMATOLOGIA Y VENEREOLOGIA",
        "67": "DIAGNOSTICO POR IMAGENES",
        "68": "EMBRIOLOGIA",
        "69": "EMERGENCIAS Y DESASTRES",
        "70": "ENDOCRINOLOGIA",
        "71": "ENDOCRINOLOGIA PEDIATRICA",
        "72": "ENDOCRINOLOGIA PEDIATRICA Y GENETICA",
        "73": "ENDOCRINOLOGIA Y NUTRICION",
        "74": "ENFERMEDADES INFECCIOSAS",
        "75": "ENFERMEDADES INFECCIOSAS Y TROPICALES",
        "76": "EPIDEMIOLOGIA",
        "77": "EPIDEMIOLOGIA DE CAMPO",
        "78": "EPIDEMIOLOGIA DE ENFERMEDADES METAXENICAS",
        "79": "FARMACOLOGIA",
        "80": "FISIATRIA",
        "81": "FISIOLOGIA",
        "82": "FLEBOLOGIA Y LINFOLOGIA",
        "83": "FONIATRIA",
        "84": "GASTROENTEROLOGIA",
        "85": "GASTROENTEROLOGIA PEDIATRICA",
        "86": "GENETICA",
        "87": "GENETICA MÉDICA",
        "88": "GERENCIA DE LA SALUD OCUPACIONAL",
        "89": "GERIATRIA",
        "90": "GESTION EN SALUD",
        "91": "GINECOLOGIA DE LA NIÑA Y ADOLESCENTE",
        "416": "GINECOLOGIA DE LA NIÑA Y ADOSLESCENTE",
        "92": "GINECOLOGIA ONCOLOGICA",
        "451": "GINECOLOGIA UNIDAD PISO PÉLVICO",
        "93": "GINECOLOGIA Y OBSTETRICIA",
        "94": "HEMATOLOGIA",
        "95": "HEMATOLOGIA CLINICA",
        "96": "HEMATOLOGIA PEDIATRICA",
        "97": "HEMATOLOGIA Y HEMOTERAPIA",
        "98": "HEPATOLOGIA",
        "99": "HIGIENE OCUPACIONAL",
        "100": "HISTOLOGIA",
        "101": "HISTOPATOLOGIA",
        "102": "IMAGENOLOGIA",
        "103": "INFECTOLOGIA",
        "104": "INFECTOLOGIA PEDIATRICA",
        "105": "INMUNOLOGIA",
        "106": "INMUNOLOGIA CLINICA Y ALERGOLOGIA",
        "107": "INMUNOLOGIA Y ALERGIA",
        "108": "INMUNOLOGIA Y REUMATOLOGIA",
        "110": "LABORATORIO CLINICO Y ANATOMIA PATOLOGICA",
        "111": "MEDICINA AEROESPACIAL",
        "112": "MEDICINA CRÍTICA",
        "113": "MEDICINA CRITICA DE ADULTO",
        "114": "MEDICINA CRÍTICA Y TERAPIA INTENSIVA",
        "418": "MEDICINA DE DEPORTE",
        "115": "MEDICINA DE EMERGENCIAS Y DESASTRES",
        "116": "MEDICINA DE ENFERMEDADES INFECCIOSAS Y TROPICALES",
        "117": "MEDICINA DE REHABILITACION",
        "118": "MEDICINA DEL DEPORTE",
        "119": "MEDICINA DEL TRABAJO",
        "120": "MEDICINA ESTETICA",
        "121": "MEDICINA FAMILIAR",
        "419": "MEDICINA FAMILIAR Y  SALUD COMUNITARIA",
        "122": "MEDICINA FAMILIAR Y COMUNITARIA",
        "123": "MEDICINA FAMILIAR Y SALUD COMUNITARIA",
        "420": "MEDICINA FISICA Y DE REHABILITACION",
        "124": "MEDICINA FISICA Y REHABILITACION",
        "125": "MEDICINA GENERAL INTEGRAL",
        "126": "MEDICINA GENERAL Y ONCOLOGICA",
        "127": "MEDICINA HIPERBARICA Y SUBACUATICA",
        "128": "MEDICINA INTEGRAL Y GESTION EN SALUD",
        "129": "MEDICINA INTENSIVA",
        "130": "MEDICINA INTENSIVA PEDIATRICA",
        "131": "MEDICINA INTENSIVA Y DE EMERGENCIA",
        "132": "MEDICINA INTERNA",
        "133": "MEDICINA INTERNA - GASTROENTEROLOGIA",
        "134": "MEDICINA INTERNA PEDIATRICA",
        "135": "MEDICINA INTERNA Y CARDIOLOGIA",
        "136": "MEDICINA INTERNA Y PEDIATRIA",
        "137": "MEDICINA LEGAL",
        "138": "MEDICINA MATERNO FETAL",
        "139": "MEDICINA NUCLEAR",
        "140": "MEDICINA OCUPACIONAL Y MEDIO AMBIENTE",
        "452": "MEDICINA PALIATIVA Y DOLOR ONCOLOGICO",
        "141": "MEDICINA PEDIATRICA",
        "142": "MEDICINA PREVENTIVA Y SALUD PÚBLICA",
        "143": "NEFROLOGIA",
        "144": "NEFROLOGIA PEDIATRICA",
        "145": "NEONATOLOGIA",
        "146": "NEUMOLOGIA",
        "147": "NEUMOLOGIA CLINICA",
        "148": "NEUMOLOGIA PEDIATRICA",
        "149": "NEUMONOLOGIA CLINICA",
        "150": "NEUMONOLOGIA Y TISIOLOGIA",
        "151": "NEUROCIRUGIA",
        "152": "NEUROCIRUGIA PEDIATRICA",
        "453": "NEUROCIRUGIA UNIDAD COLUMNA Y MÉDULA ESPINAL",
        "153": "NEUROFISIOLOGIA CLINICA",
        "154": "NEUROLOGIA",
        "155": "NEUROLOGIA PEDIATRICA",
        "157": "NUTRICION CON ORIENTACION EN OBESIDAD",
        "158": "OFTALMOLOGIA",
        "421": "OFTALMOLOGIA  PEDIATRICA Y ESTRABISMO",
        "159": "OFTALMOLOGIA ONCOLOGICA",
        "454": "OFTALMOLOGIA PEDIATRICA",
        "160": "OFTALMOLOGIA PEDIATRICA Y ESTRABISMO",
        "161": "ONCOLOGIA",
        "162": "ONCOLOGIA CLINICA",
        "163": "ONCOLOGIA MÉDICA",
        "164": "ONCOLOGIA PEDIATRICA",
        "165": "ONCOLOGIA QUIRURGICA",
        "166": "ONCOLOGIA RADIOTERAPICA",
        "167": "ORTOPEDIA ONCOLOGICA",
        "168": "ORTOPEDIA Y TRAUMATOLOGIA",
        "169": "OTORRINOLARINGOLOGIA",
        "170": "OTORRINOLARINGOLOGIA PEDIATRICA",
        "171": "OTORRINOLARINGOLOGIA Y CIRUGIA DE CABEZA Y CUELLO",
        "172": "PARASITOLOGIA",
        "173": "PATOLOGIA",
        "174": "PATOLOGIA CLINICA",
        "175": "PATOLOGIA ONCOLOGICA",
        "176": "PATOLOGIA Y LABORATORIO CLINICO",
        "177": "PEDIATRIA",
        "178": "PEDIATRIA DE EMERGENCIAS Y DESASTRES",
        "429": "PEDIATRÍA Y NEONATOLOGIA",
        "179": "PEDIATRIA Y PUERICULTURA",
        "455": "PODOLOGIA",
        "180": "PROCTOLOGIA",
        "181": "PSIQUIATRIA",
        "182": "PSIQUIATRIA  DE NIÑOS Y ADOLESCENTES",
        "422": "PSIQUIATRIA DE NIÑOS Y ADOSLESCENTES",
        "183": "PSIQUIATRIA EN ADICCIONES",
        "184": "RADIODIAGNOSTICO",
        "185": "RADIOLOGIA",
        "186": "RADIOLOGIA E IMAGEN",
        "187": "RADIOLOGIA INTERVENCIONISTA",
        "188": "RADIOLOGIA Y DIAGNOSTICO POR IMAGENES",
        "189": "RADIOTERAPIA",
        "190": "REUMATOLOGIA",
        "457": "REUMATOLOGIA PEDIATRICA",
        "191": "SALUD OCUPACIONAL",
        "192": "SALUD OCUPACIONAL E HIGIENE DEL AMBIENTE LABORAL",
        "193": "SALUD PÚBLICA",
        "194": "SALUD PÚBLICA CON MENCION EN EPIDEMIOLOGIA",
        "195": "TERAPEUTICAS ALTERNATIVAS Y FARMACOLOGIA VEGETAL",
        "196": "TERAPIA INTENSIVA",
        "197": "TOCOGINECOLOGIA",
        "198": "TOXICOLOGIA",
        "199": "TOXICOLOGIA MÉDICA",
        "430": "TRAUMATOLOGIA",
        "458": "TRAUMATOLOGIA UNIDAD COLUMNA Y MÉDULA ESPINAL",
        "200": "UROLOGIA",
        "423": "UROLOGIA GENERAL Y ONCOLOGIA",
        "201": "UROLOGIA GENERAL Y ONCOLOGICA",
        "202": "UROLOGIA ONCOLOGICA",
        "203": "UROLOGIA PEDIATRICA",
        "459": "UROLOGIA UNIDAD PISO PÉLVICO",
        "204": "VENEREOLOGIA"
    }
}

def limpiar_nombre_archivo(texto):
    if not texto:
        return 'desconocido'
    nfkd_form = unicodedata.normalize('NFKD', texto)
    texto_sin_tildes = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return re.sub(r'[^a-zA-Z0-9]', '_', texto_sin_tildes).lower()

def load_profession_resources(nombre):
    profesion = PROFESION_MAP.get(nombre)
    if profesion is None:
        raise ValueError('Profesion no soportada')
    headers = HEADERS_MAP[nombre]
    cookies = COOKIES_MAP[nombre]
    especialidades = ESPECIALIDADES_MAP[nombre]
    return profesion, headers, cookies, especialidades

def extraer_por_especialidad(headers, cookies: Optional[dict], params):
    all_data = []
    response = None
    for intento in range(3):
        try:
            response = requests.get(BASE_URL, params=params, headers=headers, cookies=cookies, verify=False, timeout=15)
            if response.status_code == 200:
                break
        except Exception:
            time.sleep(2)
    if response is None or response.status_code != 200:
        return []
    data = response.json()
    if not data.get('success'):
        return []
    total_registros = data.get('total', 0)
    if not total_registros:
        return []
    total_paginas = math.ceil(total_registros / int(params.get('size', '10')))
    for pagina in range(total_paginas):
        params['page'] = str(pagina)
        try:
            resp = requests.get(BASE_URL, params=params, headers=headers, cookies=cookies, verify=False, timeout=15)
            page_data = resp.json()
            if page_data.get('data'):
                all_data.extend(page_data['data'])
            time.sleep(0.1)
        except Exception:
            pass
    return all_data

def run_extraccion(nombre_profesion, feInicio, feFin, ubigeo, size, nombreIpress, out_dir):
    profesion, headers, cookies, especialidades = load_profession_resources(nombre_profesion)
    count = 0
    frames = []
    for id_esp, nombre_esp in especialidades.items():
        count += 1
        params = {
            'feInicio': feInicio,
            'feFin': feFin,
            'profesion': profesion,
            'especialidad': id_esp,
            'nombreIpress': nombreIpress or '',
            'nombre': '',
            'paterno': '',
            'materno': '',
            'ubigeo': ubigeo,
            'size': str(size),
            'page': '0'
        }
        datos = extraer_por_especialidad(headers, cookies, params)
        if not datos:
            continue
        df = pd.json_normalize(datos)
        filename = f"{out_dir}/susalud_{limpiar_nombre_archivo(nombre_profesion)}_{limpiar_nombre_archivo(nombre_esp)}_lima.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    combined.to_csv(f"{out_dir}/SASALUD_DATA_LIMA.csv", index=False, encoding='utf-8-sig')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profesion', required=True, choices=list(PROFESION_MAP.keys()))
    parser.add_argument('--feInicio', default='2025-11-21')
    parser.add_argument('--feFin', default='2025-12-20')
    parser.add_argument('--ubigeo', default='15')
    parser.add_argument('--size', type=int, default=10)
    parser.add_argument('--nombreIpress', default='')
    parser.add_argument('--out_dir', default='.')
    args = parser.parse_args()
    run_extraccion(args.profesion, args.feInicio, args.feFin, args.ubigeo, args.size, args.nombreIpress, args.out_dir)

if __name__ == '__main__':
    main()
