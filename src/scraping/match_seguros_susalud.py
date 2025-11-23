import pandas as pd
from difflib import SequenceMatcher
import re
import unicodedata
import argparse

def norm(t):
    t = str(t).upper().strip()
    t = ''.join(ch for ch in unicodedata.normalize('NFD', t) if not unicodedata.combining(ch))
    t = re.sub(r'[^A-Z0-9 ]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def build_matches(seguros_df, susalud_df, col_seg, col_med, threshold):
    susalud_df['codigo_Unico'] = susalud_df['codigo_Unico'].astype(str).str.extract('([0-9]+)', expand=False).str.zfill(8)
    names_med = pd.Series(susalud_df[col_med].dropna().astype(str).str.upper().str.strip().unique().tolist())
    meds_norm = names_med.apply(norm)
    names_seg = seguros_df[col_seg].astype(str).str.upper().str.strip().unique().tolist()
    results = []
    for n in names_seg:
        nn = norm(n)
        best = None
        best_score = 0.0
        for m, mn in zip(names_med.tolist(), meds_norm.tolist()):
            s = SequenceMatcher(None, nn, mn).ratio()
            if s > best_score:
                best_score = s
                best = m
        results.append({'seguro_nombre_clinica': n, 'susalud_establecimiento': best, 'score': best_score})
    matches = pd.DataFrame(results)
    code_map = susalud_df.assign(_norm=susalud_df[col_med].astype(str).apply(norm)).groupby('_norm')['codigo_Unico'].agg(lambda s: s.dropna().astype(str).iloc[0] if len(s.dropna()) > 0 else None).to_dict()
    matches['_med_norm'] = matches['susalud_establecimiento'].astype(str).apply(norm)
    matches['codigo_Unico'] = matches['_med_norm'].map(code_map)
    matches_valid = matches[(matches['codigo_Unico'].notna()) & (matches['score'] >= threshold)].copy()
    return matches_valid

def enrich_seguros(seguros_df, matches_valid, col_seg):
    seguros_df[col_seg] = seguros_df[col_seg].astype(str).str.upper().str.strip()
    for c in ['codigo_Unico', 'codigo_Unico_x', 'codigo_Unico_y']:
        if c in seguros_df.columns:
            seguros_df.drop(columns=[c], inplace=True)
    right_df = matches_valid[['seguro_nombre_clinica', 'codigo_Unico', 'susalud_establecimiento', 'score']].rename(columns={'codigo_Unico': 'codigo_Unico_match'})
    seguros_matched = seguros_df.merge(right_df, left_on=col_seg, right_on='seguro_nombre_clinica', how='left')
    seguros_matched['codigo_Unico'] = seguros_matched['codigo_Unico_match']
    seguros_matched.drop(columns=['seguro_nombre_clinica', 'codigo_Unico_match'], inplace=True)
    seguros_matched = seguros_matched[seguros_matched['codigo_Unico'].notna()].copy()
    return seguros_matched

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--susalud', default='src/scraping/SUSALUD_DATA_LIMA.csv')
    parser.add_argument('--seguros', default='src/scraping/SEGUROS.csv')
    parser.add_argument('--threshold', type=float, default=0.80)
    parser.add_argument('--output', default='src/scraping/SEGUROS_matched.csv')
    args = parser.parse_args()
    df = pd.read_csv(args.susalud, dtype={'codigo_Unico': str})
    seguros = pd.read_csv(args.seguros)
    col_med = 'establecimiento' if 'establecimiento' in df.columns else 'Establecimiento'
    col_seg = 'nombre_clinica' if 'nombre_clinica' in seguros.columns else next((c for c in ['Clinica', 'clinica', 'nombre', 'Nombre'] if c in seguros.columns), None)
    if col_seg is None:
        raise ValueError('No se encontró columna de nombre en SEGUROS')
    matches_valid = build_matches(seguros, df, col_seg, col_med, args.threshold)
    seguros_enriched = enrich_seguros(seguros, matches_valid, col_seg)
    print('Establecimientos con seguros RIMAC:', seguros_enriched.shape[0])
    print(seguros_enriched[['nombre_clinica', 'codigo_Unico', 'susalud_establecimiento', 'Seguro']].head(20).to_string(index=False))
    seguros_enriched.to_csv(args.output, index=False)
    print('Archivo guardado:', args.output)

if __name__ == '__main__':
    main()
