#En este archivo se lee un archivo CSV y se convierte a JSON
import os
import csv
import json

def read_csv_files(folder_path):
    revistas = {}

    # Leer archivos de áreas
    areas_file = os.path.join(folder_path, 'areas', 'areas.csv')
    with open(areas_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            revista = row['titulo']
            area = row['area']
            if revista not in revistas:
                revistas[revista] = {'areas': [], 'catalogos': []}
            revistas[revista]['areas'].append(area)

    # Leer archivos de catálogos
    catalogos_file = os.path.join(folder_path, 'catalogos', 'catalogos.csv')
    with open(catalogos_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            revista = row['titulo']
            catalogo = row['catalogo']
            if revista not in revistas:
                revistas[revista] = {'areas': [], 'catalogos': []}
            revistas[revista]['catalogos'].append(catalogo)

    return revistas


def guardar_json(data, salida):
    with open(salida, 'w', encoding='utf-8') as json_file: # Abre el archivo en modo escritura
        json.dump(data, json_file, ensure_ascii=False, indent=4)  # Escribe los datos en formato JSON




def main():
    folder = 'datos/csv'
    salida = 'datos/json/revistas.json'
    
    revistas = read_csv_files(folder)
    guardar_json(revistas, salida)
    
    # Verificar que el archivo JSON puede ser leído
    with open(salida, 'r', encoding='utf-8') as json_file:
        loaded_data = json.load(json_file)
        print("Datos cargados desde JSON:", loaded_data)

if __name__ == "__main__":
    main()
