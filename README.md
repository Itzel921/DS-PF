# 🧠 Sistema de Exploración de Revistas Científicas - UNISON

Este proyecto permite explorar revistas académicas según su área, catálogo y otros criterios. Utiliza Python, Flask y Bootstrap, y está basado en datos de SCImago y Resurchify.

## 📁 Estructura del Proyecto

```

proyecto/
│
├── datos/
│   ├── csv/
│   │   ├── areas/
│   │   └── catalogos/
│   └── json/
│       ├── revistas.json
│       └── scimagojr.json
│
├── scraper/             # Web scraper para SCImago
├── frontend/            # Flask + Bootstrap (parte web)
├── utils/               # Funciones comunes
├── static/              # Archivos CSS / JS / imágenes
├── templates/           # HTML con Jinja
├── app.py               # Archivo principal de Flask
└── requirements.txt

````

## 🚀 Instrucciones para ejecutar

1. Clona este repositorio:
   ```bash
   git clone https://github.com/usuario/repositorio.git
   cd repositorio


2. Crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   flask run
   ```

> Asegúrate de tener Python 3.9 o superior.

## 🚀 Funcionalidades Implementadas

* ✅ Lectura de archivos JSON para cargar datos de revistas y SCImago.
* ✅ Interfaz web con Flask + Bootstrap.
* ✅ Exploración por área, catálogo, letra y búsqueda.
  - **Áreas**: Lista de áreas disponibles con enlaces a las revistas asociadas.
  - **Catálogos**: Lista de catálogos disponibles con enlaces a las revistas asociadas.
  - **Explorar por Letra**: Tabla dinámica de revistas que inician con una letra específica.
  - **Búsqueda**: Tabla dinámica con resultados basados en palabras clave.
* ✅ Créditos: Página con los nombres y fotos de los desarrolladores.

## 📄 Rutas Principales

| Ruta            | Descripción                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `/`             | Página de inicio con introducción al sistema.                              |
| `/areas`        | Lista de áreas disponibles.                                                |
| `/catalogos`    | Lista de catálogos disponibles.                                            |
| `/explorar`     | Abecedario con enlaces para explorar revistas por letra inicial.           |
| `/buscar`       | Página de búsqueda con resultados dinámicos.                              |
| `/creditos`     | Página con los créditos del equipo desarrollador.                         |
| `/area/<area>`  | Detalles de las revistas asociadas a un área específica.                  |
| `/catalogo/<catalogo>` | Detalles de las revistas asociadas a un catálogo específico.        |
| `/explorar/<letra>` | Tabla de revistas que inician con una letra específica.                |
| `/revista/<titulo>` | Detalles completos de una revista específica.                         |

## 🧪 Instrucciones para Pruebas

1. **Explorar Áreas**:
   - Accede a `/areas` para ver la lista de áreas.
   - Haz clic en un área para ver las revistas asociadas.

2. **Explorar Catálogos**:
   - Accede a `/catalogos` para ver la lista de catálogos.
   - Haz clic en un catálogo para ver las revistas asociadas.

3. **Explorar por Letra**:
   - Accede a `/explorar` y selecciona una letra para ver las revistas que inician con esa letra.

4. **Buscar Revistas**:
   - Accede a `/buscar` e ingresa palabras clave para buscar revistas.

5. **Ver Detalles de una Revista**:
   - Haz clic en el título de una revista en cualquier tabla para ver sus detalles completos.

---

## 🔍 Funcionalidades planeadas

* ✅ Lectura de archivos CSV y creación de `revistas.json`
* 🔄 Web scraper para obtener información de SCImago y Resurchify
* 🖥️ Interfaz web con Flask + Bootstrap
* 🔍 Exploración por área, catálogo, letra y búsqueda
* 🧾 Créditos y presentación
* 🔐 Login de usuario (extra)
* ♻️ Cacheo y actualización mensual de datos (extra)

## 🌿 Ramas del Proyecto

El proyecto está organizado en las siguientes ramas para facilitar el desarrollo colaborativo:

* `main`: Rama principal con la versión estable del proyecto.
* `parte1-json`: Implementación de la funcionalidad para convertir archivos CSV a JSON.
* `parte2-scraper`: Desarrollo del web scraper para obtener datos de SCImago y Resurchify.
* `parte3-frontend`: Creación de la interfaz web utilizando Flask y Bootstrap.
* `login-feature`: Implementación del sistema de login para usuarios.
* `actualizar-cache`: Funcionalidad para la actualización mensual de datos con seguimiento de la última visita.

---

## 👨‍💻 Integrantes del equipo

Moises Perez Aello
Itzel Alejandra Monroy Alvarez

## 🤖 Asistentes digitales utilizados

Durante el desarrollo de este proyecto, se hizo uso de asistentes digitales como **ChatGPT** y **Copilot** para organizar el flujo de trabajo, generar código base y refinar funcionalidades. Todas las decisiones de diseño y desarrollo fueron supervisadas por los integrantes del equipo.

## 🏫 Universidad de Sonora

Este sistema fue desarrollado como parte del proyecto final para la materia de Desarrollo de Sistemas, bajo el marco institucional de la Universidad de Sonora.


