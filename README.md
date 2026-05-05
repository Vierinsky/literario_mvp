# Literario MVP

Proyecto Django para explorar un recomendador literario de fantasía y ciencia ficción basado en texto libre, filtros editoriales y una capa inicial de curaduría.

## Estado actual

El proyecto ya incluye:

- home pública con formulario de búsqueda
- búsqueda básica por texto libre y filtros
- ranking simple por score
- catálogo curado con autores, libros y tags
- tracking de búsquedas y resultados
- captura de email con consentimiento
- sección editorial mínima
- Django admin operativo

## Stack

- Python
- Django
- SQLite por ahora
- Templates de Django
- CSS simple
- Lógica de recomendación en servicios Python

## Apps principales

- `core`: páginas públicas y flujo web principal
- `catalog`: autores, libros y tags curatoriales
- `recommendations`: lógica de búsqueda, normalización y ranking
- `tracking`: persistencia de búsquedas y resultados
- `subscribers`: captura de email y consentimiento
- `editorial`: notas editoriales y relación con libros

## Cómo ejecutar el proyecto

1. Crear y activar entorno virtual
2. Instalar dependencias
3. Ejecutar migraciones
4. Crear superusuario si hace falta
5. Levantar servidor

### Entorno virtual
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1