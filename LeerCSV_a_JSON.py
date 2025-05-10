#En este archivo se lee el csv y se genera el json

import os
import csv
import json

# Carpetas de entrada y salida
csv_areas_path = "datos/csv/areas"
csv_catalogos_path = "datos/csv/catalogos"
json_output_path = "datos/json/revistas.json"

revistas_dict = {}

# Función auxiliar para agregar datos
def agregar_info(ruta, tipo):
    for archivo in os.listdir(ruta):
        if archivo.endswith(".csv"):
            try:
                # Intentar primero con UTF-8
                with open(os.path.join(ruta, archivo), encoding="utf-8") as f:
                    reader = csv.reader(f)
                    process_file(reader, tipo)
            except UnicodeDecodeError:
                # Si falla, intentar con latin-1
                with open(os.path.join(ruta, archivo), encoding="latin-1") as f:
                    reader = csv.reader(f)
                    process_file(reader, tipo)

def process_file(reader, tipo):
    next(reader)  # saltar encabezado si lo tiene
    for row in reader:
        if len(row) >= 2:  # Verificar que hay al menos 2 columnas
            titulo = row[0].strip().lower()
            valor = row[1].strip()
            if titulo not in revistas_dict:
                revistas_dict[titulo] = {"areas": [], "catalogos": []}
            if valor not in revistas_dict[titulo][tipo]:
                revistas_dict[titulo][tipo].append(valor)

# Crear directorios si no existen
os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

# Leer áreas y catálogos
agregar_info(csv_areas_path, "areas")
agregar_info(csv_catalogos_path, "catalogos")

# Guardar como JSON
with open(json_output_path, "w", encoding="utf-8") as json_file:
    json.dump(revistas_dict, json_file, indent=2, ensure_ascii=False)

print(f"JSON generado correctamente en: {json_output_path}")
