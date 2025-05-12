import os
import json
import time
import requests
import argparse
import re
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurar rutas absolutas
INPUT_JSON = os.path.join(BASE_DIR, 'datos', 'json', 'revistas.json')
OUTPUT_JSON = os.path.join(BASE_DIR, 'datos', 'json', 'revistas_resurchify.json')
BACKUP_JSON = os.path.join(BASE_DIR, 'datos', 'json', 'revistas_resurchify_backup.json')

# Configurar argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Scraper de Resurchify con punto de inicio configurable')
parser.add_argument('--inicio', type=int, default=0, help='Índice desde donde empezar a procesar (default: 0)')
parser.add_argument('--fin', type=int, help='Índice donde terminar de procesar (opcional)')
parser.add_argument('--reverso', action='store_true', help='Procesar las revistas en orden inverso')
args = parser.parse_args()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

RESURCHIFY_BASE_URL = 'https://www.resurchify.com'
SEARCH_URL = RESURCHIFY_BASE_URL + '/find/search/'  # El endpoint de búsqueda
JOURNAL_URL = RESURCHIFY_BASE_URL + '/impact/details/'  # El endpoint de detalles de revista

# Constantes para símbolos de log
LOG_SUCCESS = "✅"
LOG_ERROR = "❌"
LOG_INFO = "ℹ️"
LOG_WARNING = "⚠️"
LOG_PROCESSING = "🔄"

def save_data_safely(data, titulo=""):
    """Guarda los datos en el archivo principal y en el backup de forma segura"""
    try:
        # Guardar en archivo principal
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Guardar en backup
        with open(BACKUP_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        if titulo:
            print(f"{LOG_SUCCESS} Datos guardados después de procesar: {titulo}")
    except Exception as e:
        print(f"{LOG_ERROR} Error al guardar datos: {str(e)}")

# Cargar revistas ya obtenidas
if os.path.exists(OUTPUT_JSON):
    print(f"{LOG_INFO} Cargando datos existentes...")
    with open(OUTPUT_JSON, 'r', encoding='utf-8') as f:
        revistas_data = json.load(f)
elif os.path.exists(BACKUP_JSON):
    print(f"{LOG_INFO} Recuperando datos del archivo de respaldo...")
    with open(BACKUP_JSON, 'r', encoding='utf-8') as f:
        revistas_data = json.load(f)
else:
    revistas_data = {}

def scrap(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code} en {url}")
    return response

def find_journal_url(journal_title):
    """Busca una revista en Resurchify y retorna su URL."""
    try:
        # Mejorar la limpieza del título
        clean_title = journal_title.lower()
        # Remover caracteres especiales pero mantener guiones y espacios
        clean_title = re.sub(r'[^a-z0-9\s-]', '', clean_title)
        # Remover palabras comunes que pueden afectar la búsqueda
        stop_words = [': ', ' and ', ' & ', ' the ']
        for word in stop_words:
            clean_title = clean_title.replace(word, ' ')
        # Normalizar espacios
        clean_title = ' '.join(clean_title.split())
        
        print(f"{LOG_INFO} Búsqueda con título limpio: {clean_title}")
        
        # Codificar el título para la URL
        search = SEARCH_URL + quote_plus(clean_title)
        response = scrap(search)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar coincidencia aproximada
        search_results = soup.select('.journal-card')
        best_match = None
        highest_ratio = 0
        
        for result in search_results:
            title_elem = result.select_one('.journal-name')
            if title_elem:
                result_title = title_elem.text.strip().lower()
                # Usar ratio de similitud para encontrar la mejor coincidencia
                ratio = len(set(clean_title.split()) & set(result_title.split())) / len(set(clean_title.split()))
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = result

        if best_match and highest_ratio > 0.5:  # Umbral de similitud del 50%
            link = best_match.select_one('a')
            if link and 'href' in link.attrs:
                journal_url = link['href']
                if not journal_url.startswith('http'):
                    journal_url = RESURCHIFY_BASE_URL + journal_url
                print(f"{LOG_SUCCESS} Coincidencia encontrada (ratio: {highest_ratio:.2f})")
                return journal_url

    except Exception as e:
        print(f"{LOG_WARNING} Error en búsqueda: {str(e)}")
    
    return None

def extract_metrics(soup):
    """Extrae las métricas de la página de la revista."""
    metrics = {}
    try:
        # Impact Factor y otros indicadores
        metrics_boxes = soup.select('.metric-box')
        for box in metrics_boxes:
            label = box.select_one('.metric-label')
            value = box.select_one('.metric-value')
            if label and value:
                key = label.text.strip().lower().replace(' ', '_')
                metrics[key] = value.text.strip()
        
        # Acceptance Rate y tiempos de revisión
        stats_section = soup.select_one('.journal-stats')
        if stats_section:
            for stat in stats_section.select('.stat-item'):
                label = stat.select_one('.stat-label')
                value = stat.select_one('.stat-value')
                if label and value:
                    key = label.text.strip().lower().replace(' ', '_')
                    metrics[key] = value.text.strip()
        
        # SCImago Quartile si está disponible
        quartile = soup.select_one('.scimago-quartile')
        if quartile:
            metrics['scimago_quartile'] = quartile.text.strip()
            
    except Exception as e:
        print(f"{LOG_ERROR} Error al extraer métricas: {e}")
    
    return metrics

def scrape_journal_data(url):
    """Extrae todos los datos disponibles de la página de la revista."""
    soup = BeautifulSoup(scrap(url).text, 'html.parser')
    
    data = {
        "resurchify_url": url,
        "metrics": extract_metrics(soup)
    }
    
    try:
        # Información básica
        header = soup.select_one('.journal-header')
        if header:
            # Título oficial
            title = header.select_one('.journal-title')
            if title:
                data['official_title'] = title.text.strip()
            
            # ISSN
            issn = header.select_one('.journal-issn')
            if issn:
                data['issn'] = issn.text.strip().replace('ISSN:', '').strip()
        
        # Publisher y otra información
        info_box = soup.select_one('.journal-info-box')
        if info_box:
            # Publisher
            publisher = info_box.select_one('.publisher-name')
            if publisher:
                data['publisher'] = publisher.text.strip()
            
            # Website oficial
            website = info_box.select_one('.journal-website')
            if website and 'href' in website.attrs:
                data['official_website'] = website['href']
            
            # Subjects/Categories
            subjects = info_box.select('.subject-category')
            if subjects:
                data['subject_categories'] = [subj.text.strip() for subj in subjects]
            
            # Open Access Status
            oa_status = info_box.select_one('.oa-status')
            if oa_status:
                data['open_access'] = oa_status.text.strip()
    
    except Exception as e:
        print(f"{LOG_ERROR} Error al extraer información general: {e}")
    
    return data

# Cargar títulos a procesar
with open(INPUT_JSON, 'r', encoding='utf-8') as f:
    revistas_input = json.load(f)

# Calcular el rango de revistas a procesar
inicio = args.inicio
fin = args.fin if args.fin is not None else len(revistas_input)
revistas_items = list(revistas_input.items())

# Si es en reverso, invertimos el orden
if args.reverso:
    revistas_items = revistas_items[::-1]
    tmp = len(revistas_items) - fin
    fin = len(revistas_items) - inicio
    inicio = tmp

print(f"{LOG_INFO} Procesando revistas del índice {inicio} al {fin}")
print(f"{LOG_INFO} Total de revistas a procesar: {fin - inicio}")

# Contador de revistas procesadas en esta ejecución
procesados_count = 0

# Procesar cada revista en el rango especificado
for titulo_revista, _ in revistas_items[inicio:fin]:
    # Si la revista ya está en los datos, la saltamos
    if titulo_revista in revistas_data:
        continue
        
    print(f"{LOG_PROCESSING} Procesando revista: {titulo_revista}")
    
    try:
        # Buscar URL de la revista en Resurchify
        url_revista = find_journal_url(titulo_revista)
        if not url_revista:
            print(f"{LOG_WARNING} No se encontró la revista: {titulo_revista}")
            continue
            
        # Obtener datos de la revista
        datos_revista = scrape_journal_data(url_revista)
        revistas_data[titulo_revista] = datos_revista
        
        # Guardar progreso después de cada revista procesada exitosamente
        save_data_safely(revistas_data, titulo_revista)
        
        procesados_count += 1
        time.sleep(2)
    except Exception as error:
        print(f"{LOG_ERROR} Error al procesar la revista {titulo_revista}: {str(error)}")

# Asegurar que los datos finales estén guardados
save_data_safely(revistas_data)
print(f"{LOG_SUCCESS} Proceso finalizado. Nuevas revistas procesadas: {procesados_count}")
print(f"{LOG_INFO} Rango procesado: {inicio} - {fin}")
