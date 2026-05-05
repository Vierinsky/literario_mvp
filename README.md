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
```
### Dependencias

```
pip install -r requirements.txt
```

### Migraciones

```
python manage.py makemigrations
python manage.py migrate
```
### Superusuario

```
python manage.py createsuperuser
```

### Runserver

```
python manage.py runserver
```
## Seed manual actual

Existe un script inicial de carga en:
```
scripts/load_seed_books.py
```

Puede ejecutarse desde Django shell con:
```
exec(open("scripts/load_seed_books.py", encoding="utf-8").read())
```

## Estado del recomendador

Actualmente el sistema usa:
- filtros explícitos (tone, pace, theme, length)
- búsqueda textual básica sobre título, sinopsis, autor y tags
- normalización simple de términos
- score heurístico para ordenar resultados

Todavía no usa embeddings.

## Pendientes principales

- formalizar seed como management command
- mejorar ranking y relevancia
- preparar embedding_text
- integrar proveedor externo de email/newsletter
- expandir catálogo
- mejorar UI/copy

## Roadmap de IA

Este proyecto no busca quedarse en una búsqueda textual con filtros.
La idea es usar esta base web y de datos como plataforma para aprender AI Engineering aplicado a recomendación literaria.

Capas previstas:

1. búsqueda híbrida inicial
   - filtros explícitos
   - normalización de texto
   - ranking heurístico

2. capa semántica
   - construcción de `embedding_text`
   - generación de embeddings del catálogo
   - similitud semántica entre búsqueda y libros

3. ranking más avanzado
   - mezcla de score semántico + metadata curada + filtros
   - mejores explicaciones
   - ajustes a partir de comportamiento real

## Deuda técnica sana

### Actual

- SQLite en vez de PostgreSQL
- seed ejecutada vía script y no management command
- ranking heurístico todavía simple
- `query_text` sin embeddings
- UI todavía básica
- falta integración real con proveedor de email
- falta tests automáticos

### Notas

Esto no bloquea el MVP actual, pero conviene tenerlo visible para iterar con orden.