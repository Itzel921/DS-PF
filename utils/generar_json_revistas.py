#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json
from pathlib import Path
import os
import unicodedata

# Definir rutas base
BASE_DIR = Path(__file__).parent.parent
AREAS_DIR = BASE_DIR / 'datos' / 'csv' / 'areas'
CATALOGOS_DIR = BASE_DIR / 'datos' / 'csv' / 'catalogos'
OUTPUT_FILE = BASE_DIR / 'datos' / 'json' / 'revistas.json'

def limpiar_titulo(titulo):
    titulo = str(titulo).lower().strip()
    titulo = unicodedata.normalize('NFKD', titulo).encode('ascii', 'ignore').decode('ascii')
    return titulo

def limpiar_nombre_area(area):
    return area.replace(' RadGridExport', '').replace('_RadGridExport', '')

def leer_csvs_areas():
    dataframes = []
    for csv_file in AREAS_DIR.glob('*.csv'):
        try:
            area_name = limpiar_nombre_area(csv_file.stem)
            for encoding in ['utf-8', 'latin1', 'cp1252']:
                try:
                    df = pd.read_csv(csv_file, encoding=encoding, names=['nombre_revista'])
                    df = df[df['nombre_revista'] != 'TITULO:']
                    df['area'] = area_name
                    dataframes.append(df)
                    print(f'Archivo {csv_file.name} leído con codificación {encoding}')
                    break
                except UnicodeDecodeError:
                    continue
        except Exception as e:
            print(f'Error al procesar {csv_file}: {e}')
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

def leer_csvs_catalogos():
    dataframes = []
    for csv_file in CATALOGOS_DIR.glob('*.csv'):
        try:
            catalogo_name = limpiar_nombre_area(csv_file.stem)
            for encoding in ['utf-8', 'latin1', 'cp1252']:
                try:
                    df = pd.read_csv(csv_file, encoding=encoding, names=['nombre_revista'])
                    df = df[df['nombre_revista'] != 'TITULO:']
                    df['catalogo'] = catalogo_name
                    dataframes.append(df)
                    print(f'Archivo {csv_file.name} leído con codificación {encoding}')
                    break
                except UnicodeDecodeError:
                    continue
        except Exception as e:
            print(f'Error al procesar {csv_file}: {e}')
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

def procesar_y_generar_json():
    print('Leyendo archivos CSV de áreas...')
    df_areas = leer_csvs_areas()

    print('Leyendo archivos CSV de catálogos...')
    df_catalogos = leer_csvs_catalogos()

    revistas_dict = {}

    if not df_areas.empty and 'nombre_revista' in df_areas.columns:
        for _, row in df_areas.iterrows():
            titulo = limpiar_titulo(row['nombre_revista'])
            area = row['area']
            
            if titulo not in revistas_dict:
                revistas_dict[titulo] = {'areas': [], 'catalogos': []}
            
            if area not in revistas_dict[titulo]['areas']:
                revistas_dict[titulo]['areas'].append(area)

    if not df_catalogos.empty and 'nombre_revista' in df_catalogos.columns:
        for _, row in df_catalogos.iterrows():
            titulo = limpiar_titulo(row['nombre_revista'])
            catalogo = row['catalogo']
            
            if titulo not in revistas_dict:
                revistas_dict[titulo] = {'areas': [], 'catalogos': []}
            
            if catalogo not in revistas_dict[titulo]['catalogos']:
                revistas_dict[titulo]['catalogos'].append(catalogo)

    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(revistas_dict, f, ensure_ascii=False, indent=2)

    print(f'\nArchivo JSON generado exitosamente en: {OUTPUT_FILE}')
    print(f'Total de revistas procesadas: {len(revistas_dict)}')

    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            data_verificacion = json.load(f)
            print('\nVerificación exitosa del archivo JSON:')
            print('Ejemplo de una entrada:')
            primer_revista = next(iter(data_verificacion.items()))
            print(json.dumps({primer_revista[0]: primer_revista[1]}, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f'Error al verificar el archivo: {e}')

if __name__ == '__main__':
    procesar_y_generar_json()
