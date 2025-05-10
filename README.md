---
```markdown
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
````

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

## 🔍 Funcionalidades planeadas

* ✅ Lectura de archivos CSV y creación de `revistas.json`
* 🔄 Web scraper para obtener información de SCImago y Resurchify
* 🖥️ Interfaz web con Flask + Bootstrap
* 🔍 Exploración por área, catálogo, letra y búsqueda
* 🧾 Créditos y presentación
* 🔐 Login de usuario (extra)
* ♻️ Cacheo y actualización mensual de datos (extra)

## 👨‍💻 Integrantes del equipo

Moises Perez Aello
Itzel Alejandra Monroy Alvarez

## 🤖 Asistentes digitales utilizados

Durante el desarrollo de este proyecto, se hizo uso de asistentes digitales como **ChatGPT** y **Copilot** para organizar el flujo de trabajo, generar código base y refinar funcionalidades. Todas las decisiones de diseño y desarrollo fueron supervisadas por los integrantes del equipo.

## 🏫 Universidad de Sonora

Este sistema fue desarrollado como parte del proyecto final para la materia de Desarrollo de Sistemas, bajo el marco institucional de la Universidad de Sonora.


