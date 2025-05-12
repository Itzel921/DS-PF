# 🧠 Sistema de Exploración de Revistas Científicas - UNISON

Este proyecto permite explorar revistas académicas según su área, catálogo y otros criterios. Utiliza Python, Flask y Bootstrap, integrando datos de SCImago y Resurchify. Incluye autenticación de usuarios y guardado de revistas favoritas.

## 📁 Estructura del Proyecto

```plaintext
proyecto/
│
├── datos/
│   ├── cache/          # Caché de páginas web scrapeadas
│   ├── csv/           # Datos en formato CSV
│   └── json/          # Datos procesados en JSON
│       ├── revistas.json
│       └── revistas_scimagojr.json
│
├── scraper/
│   ├── resurchify_scraper.py  # Scraper para Resurchify
│   └── sjr_scraper.py         # Scraper para SCImago
│
├── static/
│   ├── css/           # Estilos CSS
│   ├── js/            # Scripts JavaScript
│   └── images/        # Imágenes del sitio
│
├── templates/         # Plantillas HTML con Jinja2
│   ├── base.html     # Plantilla base
│   ├── index.html    # Página principal
│   ├── areas.html    # Vista de áreas
│   └── ...           # Otras plantillas
│
├── utils/            # Utilidades y helpers
│   ├── combine_results.py
│   └── generar_json_revistas.py
│
├── instance/         # Datos de la instancia
│   └── users.db      # Base de datos SQLite
│
├── app.py           # Aplicación principal Flask
├── config.py        # Configuración de la aplicación
└── requirements.txt # Dependencias del proyecto

````

## 🚀 Instrucciones para ejecutar

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Itzel921/DS-PF
   cd DS-PF


2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Unix o MacOS:
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

> 📌 Requisitos: Python 3.9 o superior

## 🌟 Características Principales

### Sistema de Exploración
* 📚 **Exploración por Áreas**:
  - Listado de áreas académicas
  - Filtrado de revistas por área
  - Visualización de métricas por área

* 📑 **Catálogos**:
  - Navegación por catálogos académicos
  - Filtrado por índices y bases de datos
  - Información detallada de indexación

* 🔤 **Exploración Alfabética**:
  - Navegación por letra inicial
  - Vista rápida de revistas
  - Ordenamiento alfabético

* 🔍 **Búsqueda Avanzada**:
  - Búsqueda por título
  - Resultados en tiempo real
  - Filtros combinados

### Sistema de Usuarios
* 👤 **Autenticación**:
  - Inicio de sesión
  - Registro de usuarios
  - Gestión de sesiones

* ⭐ **Funciones de Usuario**:
  - Guardar revistas favoritas
  - Historial de búsquedas
  - Personalización de perfil

## 📡 API y Rutas

### Rutas Públicas
| Ruta | Método | Descripción |
|------|---------|------------|
| `/` | GET | Página principal |
| `/areas` | GET | Lista de áreas |
| `/catalogos` | GET | Lista de catálogos |
| `/explorar` | GET | Exploración alfabética |
| `/buscar` | GET | Búsqueda de revistas |
| `/creditos` | GET | Página de créditos |

### Rutas Dinámicas
| Ruta | Método | Descripción |
|------|---------|------------|
| `/area/<area>` | GET | Revistas por área |
| `/catalogo/<catalogo>` | GET | Revistas por catálogo |
| `/explorar/<letra>` | GET | Revistas por inicial |
| `/revista/<titulo>` | GET | Detalles de revista |

### Rutas de Usuario
| Ruta | Método | Descripción |
|------|---------|------------|
| `/login` | GET/POST | Inicio de sesión |
| `/perfil` | GET | Perfil de usuario |
| `/logout` | GET | Cerrar sesión |
| `/add_to_profile` | POST | Guardar revista |

## 🌿 Estructura de Ramas

* `main`: Versión estable del proyecto
* `feature/json-data-structure`: Manejo de datos JSON
* `feature/scimagojr-scraper`: Scraper de SCImago
* `feature/flask-frontend`: Interfaz web
* `feature/user-authentication`: Sistema de usuarios

## 🛠️ Tecnologías Utilizadas

* **Backend**: Python, Flask
* **Frontend**: HTML, CSS, Bootstrap, JavaScript
* **Base de Datos**: SQLite, JSON
* **Herramientas**: Git, Virtual Environment
* **Bibliotecas**: flask-session, pathlib, requests

## 👥 Equipo de Desarrollo

* Moises Perez Aello
* Alberto Yahir Renteria Luna
* Itzel Alejandra Monroy Alvarez

## 🎓 Información Académica

**Universidad**: Universidad de Sonora  
**Materia**: Desarrollo de Sistemas IV  
**Semestre**: 4to  
**Periodo**: 2025

🔍 **Nota**: Este proyecto utiliza datos de SCImago Journal & Country Rank y Resurchify para propósitos académicos.


