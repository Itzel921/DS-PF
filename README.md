# DS-PF
Proyecto final de la materia Desarrollo de Sistemas IV

Este proyecto consiste en el desarrollo de una aplicación web en Python, enfocada en la gestión y visualización de información sobre revistas científicas. Está dividido en tres partes principales:

Procesamiento de Archivos CSV: Se leen archivos CSV de áreas y catálogos para construir un diccionario de revistas con sus respectivas áreas y catálogos, el cual se guarda como archivo JSON.

Web Scraping: Se implementa un scrapper que consulta información de cada revista desde el sitio scimagojr.com, complementando los datos del JSON con atributos como H-Index, ISSN, publisher, entre otros.

Interfaz Web: Se desarrolla una aplicación web con Flask + Bootstrap que permite explorar, buscar y visualizar revistas por áreas, catálogos, o de forma alfabética. El sitio incluye filtros, búsqueda dinámica, y una interfaz profesional con los colores institucionales de la Universidad de Sonora.
