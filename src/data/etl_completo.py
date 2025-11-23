#!/usr/bin/env python3
"""
Orquesta el ETL completo:
1) Normaliza SUSALUD_DATA_LIMA.csv -> instituciones, profesionales, servicios.
2) Normaliza data_lima_codigos_listos.csv -> medicamentos, medic_inst.
3) Normaliza SEGUROS_matched.csv -> asegurado.
4) Opcionalmente carga todo a Postgres (BD rimac).

Uso:
  python3 etl_completo.py          # solo genera CSV
  python3 etl_completo.py --load   # genera y carga todo a Postgres
"""
import argparse
import csv
import io
import os
from pathlib import Path
from dotenv import load_dotenv

# Fuentes
SRC_SUSALUD = Path("data_profesionales.csv")
SRC_MED = Path("data_medicamentos.csv")
SRC_SEG = Path("data_seguros.csv")
SRC_INST_META = Path("data_instituciones.csv")

# Destino
DATA_DIR = Path("clean")
CSV_INST = DATA_DIR / "institucion.csv"
CSV_PROF = DATA_DIR / "profesional.csv"
CSV_SERV = DATA_DIR / "servicio.csv"
CSV_MED = DATA_DIR / "medicamentos.csv"
CSV_MED_INST = DATA_DIR / "medic_inst.csv"
CSV_ASEG = DATA_DIR / "asegurado.csv"


def build_susalud():
    DATA_DIR.mkdir(exist_ok=True)
    instituciones = {}
    profesionales = {}
    servicios = {}

    with SRC_SUSALUD.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cod = (row.get("codigo_Unico") or "").strip()
            cmp = (row.get("cmp") or "").strip()
            profesion = (row.get("profesion") or "").strip()

            if cod:
                instituciones.setdefault(
                    cod,
                    {
                        "cod_unico": cod,
                        "direccion": (row.get("direccion") or "").strip(),
                        "institucion": (row.get("institucion") or "").strip(),
                        "establecimiento": (row.get("establecimiento") or "").strip(),
                    },
                )

            if cmp:
                profesionales.setdefault(
                    (cmp, profesion),
                    {
                        "cmp": cmp,
                        "profesion": profesion,
                        "nombre_profesional": (row.get("nombre_Profesional") or "").strip(),
                        "especialidad": (row.get("especialidad") or "").strip(),
                    },
                )

            if cod and cmp:
                servicio = (row.get("servicio") or "").strip()
                key = (cod, cmp, profesion, servicio)
                servicios.setdefault(
                    key,
                    {
                        "cod_unico": cod,
                        "cmp": cmp,
                        "profesion": profesion,
                        "servicio": servicio,
                        "detalle": (row.get("detalle") or "").strip(),
                        "telefono": (row.get("telefono") or "").strip(),
                        "actividad": (row.get("actividad") or "").strip(),
                    },
                )

    inst_meta = {}
    if SRC_INST_META.exists():
        with SRC_INST_META.open(newline="", encoding="utf-8-sig") as meta_file:
            meta_reader = csv.DictReader(meta_file)
            for row in meta_reader:
                cod = (row.get("ID") or "").strip()
                if not cod:
                    continue
                inst_meta[cod] = {
                    "files": (row.get("FILES") or "").strip(),
                    "clasificacion": (row.get("CLASIFICACION") or "").strip(),
                    "correo": (row.get("CORREO") or "").strip(),
                    "longitud": (row.get("LONGITUD") or "").strip(),
                    "latitud": (row.get("LATITUD") or "").strip(),
                    "pagina": (row.get("PAGINA") or "").strip(),
                }

    for cod, inst in instituciones.items():
        meta = inst_meta.get(cod, {})
        inst["files"] = meta.get("files", "")
        inst["clasificacion"] = meta.get("clasificacion", "")
        inst["correo"] = meta.get("correo", "")
        inst["longitud"] = meta.get("longitud", "")
        inst["latitud"] = meta.get("latitud", "")
        inst["pagina"] = meta.get("pagina", "")

    def write_csv(path: Path, fieldnames, rows):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    write_csv(
        CSV_INST,
        [
            "cod_unico",
            "direccion",
            "institucion",
            "establecimiento",
            "files",
            "clasificacion",
            "correo",
            "longitud",
            "latitud",
            "pagina",
        ],
        instituciones.values(),
    )
    write_csv(
        CSV_PROF,
        ["cmp", "profesion", "nombre_profesional", "especialidad"],
        profesionales.values(),
    )
    write_csv(
        CSV_SERV,
        ["cod_unico", "cmp", "profesion", "servicio", "detalle", "telefono", "actividad"],
        servicios.values(),
    )
    print(f"SUSALUD -> {CSV_INST}, {CSV_PROF}, {CSV_SERV}")


def normalize_date(val: str) -> str:
    val = (val or "").strip()
    if not val:
        return ""
    return val.split()[0]


def build_medicamentos():
    medicamentos = {}
    relaciones = {}

    with SRC_MED.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            codigo_med = (row.get("CODIGO_MED") or "").strip()
            if codigo_med:
                medicamentos.setdefault(
                    codigo_med,
                    {
                        "codigo_med": codigo_med,
                        "nombre_med": (row.get("NOMBRE_MED") or "").strip(),
                        "formaf": (row.get("FORMAF") or "").strip(),
                        "tipomed": (row.get("TIPOMED") or "").strip(),
                    },
                )

            cod_unico = (row.get("CODIGO_PRE") or "").strip()
            if cod_unico and codigo_med:
                key = (cod_unico, codigo_med)
                relaciones.setdefault(
                    key,
                    {
                        "cod_unico": cod_unico,
                        "codigo_med": codigo_med,
                        "stock_tot": (row.get("STOCK_TOT") or "").strip(),
                        "indicador": (row.get("INDICADOR") or "").strip(),
                        "precio": (row.get("PRECIO") or "").strip(),
                        "fecha_venc": normalize_date(row.get("FECHA_VENC")),
                    },
                )

    def write_csv(path: Path, fieldnames, rows):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    write_csv(CSV_MED, ["codigo_med", "nombre_med", "formaf", "tipomed"], medicamentos.values())
    write_csv(
        CSV_MED_INST,
        ["cod_unico", "codigo_med", "stock_tot", "indicador", "precio", "fecha_venc"],
        relaciones.values(),
    )
    print(f"Medicamentos -> {CSV_MED}, {CSV_MED_INST}")


def build_asegurado():
    asegurados = {}

    with SRC_SEG.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cod = (row.get("codigo_Unico") or "").strip()
            seguro = (row.get("Seguro") or "").strip()
            if not cod or not seguro:
                continue
            key = (cod, seguro)
            costo = (row.get("costo_consulta") or "").strip()
            if costo.lower().startswith("s/"):
                costo = costo[2:].strip()

            asegurados.setdefault(
                key,
                {
                    "cod_unico": cod,
                    "seguro": seguro,
                    "red": (row.get("red") or "").strip(),
                    "costo_consulta": costo,
                },
            )

    with CSV_ASEG.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cod_unico", "seguro", "red", "costo_consulta"])
        writer.writeheader()
        writer.writerows(asegurados.values())

    print(f"Seguros -> {CSV_ASEG}")


def load_psycopg2():
    try:
        import psycopg2  # type: ignore
        from psycopg2 import sql  # type: ignore
    except ImportError as exc:
        raise SystemExit("psycopg2 no está instalado; ejecuta `pip install psycopg2-binary` para usar --load") from exc
    return psycopg2, sql

def connect():
    # Cargar variables desde ../.env si existe (relativo a este archivo)
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    print(f"Cargando variables de entorno desde {env_path}")
    load_dotenv(dotenv_path=env_path)

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    dbname = os.getenv("POSTGRES_DB", "rimac")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "313916")

    print(f"Conectando a Postgres en {host}:{port}, base de datos '{dbname}', usuario '{user}'")

    psycopg2, _ = load_psycopg2()
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )

def ensure_schema(conn):
    _, sql = load_psycopg2()
    ddl = """
    CREATE TABLE IF NOT EXISTS institucion (
        cod_unico TEXT PRIMARY KEY,
        direccion TEXT,
        institucion TEXT,
        establecimiento TEXT,
        files TEXT,
        clasificacion TEXT,
        correo TEXT,
        longitud FLOAT,
        latitud FLOAT,
        pagina TEXT
    );
    CREATE TABLE IF NOT EXISTS profesional (
        cmp TEXT,
        profesion TEXT,
        nombre_profesional TEXT,
        especialidad TEXT,
        PRIMARY KEY (cmp, profesion)
    );
    CREATE TABLE IF NOT EXISTS servicio (
        cod_unico TEXT REFERENCES institucion(cod_unico),
        cmp TEXT,
        profesion TEXT,
        servicio TEXT,
        detalle TEXT,
        telefono TEXT,
        actividad TEXT,
        PRIMARY KEY (cod_unico, cmp, profesion, servicio),
        FOREIGN KEY (cmp, profesion) REFERENCES profesional(cmp, profesion)
    );
    CREATE TABLE IF NOT EXISTS medicamentos (
        codigo_med TEXT PRIMARY KEY,
        nombre_med TEXT,
        formaf TEXT,
        tipomed TEXT
    );
    CREATE TABLE IF NOT EXISTS medic_inst (
        cod_unico TEXT REFERENCES institucion(cod_unico),
        codigo_med TEXT REFERENCES medicamentos(codigo_med),
        stock_tot NUMERIC,
        indicador TEXT,
        precio NUMERIC,
        fecha_venc DATE,
        PRIMARY KEY (cod_unico, codigo_med)
    );
    CREATE TABLE IF NOT EXISTS asegurado (
        cod_unico TEXT REFERENCES institucion(cod_unico),
        seguro TEXT,
        red TEXT,
        costo_consulta NUMERIC,
        PRIMARY KEY (cod_unico, seguro)
    );
    """
    with conn, conn.cursor() as cur:
        cur.execute(ddl)


def copy_csv(conn, table, columns, path: Path):
    _, sql = load_psycopg2()
    copy_sql = sql.SQL(
        "COPY {} ({}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',')"
    ).format(sql.Identifier(table), sql.SQL(",").join(map(sql.Identifier, columns)))

    with path.open("r", encoding="utf-8") as f, conn.cursor() as cur:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        if header == columns:
            f.seek(0)
            cur.copy_expert(copy_sql, f)
        else:
            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=columns)
            writer.writeheader()
            for row in reader:
                writer.writerow({c: row.get(c, "") for c in columns})
            buf.seek(0)
            cur.copy_expert(copy_sql, buf)
    conn.commit()
    print(f"Cargado {path} -> {table}")


def filter_by_institucion(conn, path: Path, columns):
    with conn.cursor() as cur:
        cur.execute("SELECT cod_unico FROM institucion")
        valid_codigos = {row[0] for row in cur.fetchall()}

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=columns)
        writer.writeheader()
        skipped = 0
        for row in reader:
            if (row.get("cod_unico") or "") in valid_codigos:
                writer.writerow({c: row.get(c, "") for c in columns})
            else:
                skipped += 1
        buf.seek(0)
    return buf, skipped


def copy_medic_inst(conn):
    columns = ["cod_unico", "codigo_med", "stock_tot", "indicador", "precio", "fecha_venc"]
    buf, skipped = filter_by_institucion(conn, CSV_MED_INST, columns)
    _, sql = load_psycopg2()
    copy_sql = sql.SQL(
        "COPY medic_inst ({}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',')"
    ).format(sql.SQL(",").join(map(sql.Identifier, columns)))
    with conn.cursor() as cur:
        cur.copy_expert(copy_sql, buf)
    conn.commit()
    print(f"Cargado medic_inst (omitidas {skipped} filas sin institucion)")


def copy_asegurado(conn):
    columns = ["cod_unico", "seguro", "red", "costo_consulta"]
    buf, skipped = filter_by_institucion(conn, CSV_ASEG, columns)
    _, sql = load_psycopg2()
    copy_sql = sql.SQL(
        "COPY asegurado ({}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',')"
    ).format(sql.SQL(",").join(map(sql.Identifier, columns)))
    with conn.cursor() as cur:
        cur.copy_expert(copy_sql, buf)
    conn.commit()
    print(f"Cargado asegurado (omitidas {skipped} filas sin institucion)")


def load_all():
    conn = connect()
    ensure_schema(conn)
    copy_csv(
        conn,
        "institucion",
        [
            "cod_unico",
            "direccion",
            "institucion",
            "establecimiento",
            "files",
            "clasificacion",
            "correo",
            "longitud",
            "latitud",
            "pagina",
        ],
        CSV_INST,
    )
    copy_csv(conn, "profesional", ["cmp", "profesion", "nombre_profesional", "especialidad"], CSV_PROF)
    copy_csv(
        conn,
        "servicio",
        ["cod_unico", "cmp", "profesion", "servicio", "detalle", "telefono", "actividad"],
        CSV_SERV,
    )
    copy_csv(conn, "medicamentos", ["codigo_med", "nombre_med", "formaf", "tipomed"], CSV_MED)
    copy_medic_inst(conn)
    copy_asegurado(conn)
    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", action="store_true", help="Carga los CSV generados a Postgres")
    args = parser.parse_args()

    build_susalud()
    build_medicamentos()
    build_asegurado()

    if args.load:
        load_all()


if __name__ == "__main__":
    main()
