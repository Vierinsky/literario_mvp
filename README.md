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

- integrar proveedor externo de email/newsletter
- expandir catálogo
- mejorar UI/copy

## Future-proofing y decisiones de arquitectura

Este proyecto está construido como un MVP, pero varias decisiones se tomaron pensando en crecimiento posterior sin sobrediseñar demasiado.

### Lo que ya quedó bien encaminado (06-05-2026)

- **Separación por apps Django**: `core`, `catalog`, `recommendations`, `tracking`, `subscribers` y `editorial` ya separan responsabilidades de forma razonable.
- **Lógica en servicios**: la búsqueda/recomendación y el tracking ya salieron de las views y viven en servicios reutilizables.
- **Catálogo curado + metadata explícita**: el sistema depende de `Book`, `BookTag` y sinopsis trabajadas, lo que facilita evolucionar desde búsqueda textual hacia búsqueda semántica.
- **`embedding_text` como representación intermedia**: antes de generar embeddings reales, cada libro ya puede representarse mediante un texto enriquecido y consistente. Esto separa claramente:
  - datos fuente,
  - representación semántica,
  - vectorización posterior.
- **Regeneración explícita**: `embedding_text` no depende de magia escondida en `save()`. Se puede reconstruir por libro o de forma masiva, lo que facilita mantenimiento y futura automatización.
- **Management command para rebuild**: existe una interfaz operativa clara para regenerar `embedding_text` desde terminal.
- **Tracking básico**: búsquedas, resultados y asociación inicial con suscriptores ya quedan persistidos, lo que permitirá mejorar ranking y producto usando comportamiento real.

### Lo que todavía es MVP y deberá evolucionar

- **Base de datos**: actualmente se usa SQLite. Más adelante convendrá migrar a PostgreSQL.
- **Seed del catálogo**: hoy existe un seed manual/script inicial. Más adelante conviene formalizarlo mejor y ampliar el catálogo.
- **Ranking**: el score actual es heurístico y útil para MVP, pero no es todavía un sistema de relevancia avanzado.
- **`query_text`**: hoy usa búsqueda textual + normalización básica. Más adelante debería combinarse con embeddings.
- **Embeddings reales**: todavía no se generan vectores. `embedding_text` deja preparado ese siguiente paso.
- **Automatización a escala**: para catálogos grandes, la regeneración de `embedding_text` y de embeddings probablemente necesitará procesamiento en lotes, versionado y jobs asíncronos.
- **Newsletter/email provider**: aún no hay integración real con proveedor externo.
- **UI**: la interfaz actual ya es usable, pero sigue siendo una capa visual simple de MVP.

### Dirección prevista

La evolución esperada del sistema es:

1. catálogo curado  
2. `embedding_text` consistente  
3. embeddings por libro  
4. búsqueda semántica  
5. ranking híbrido:
   - similitud semántica
   - filtros explícitos
   - tags curatoriales
   - comportamiento real de usuarios

La idea no es sobreconstruir desde el inicio, sino crecer por capas manteniendo una base ordenada.

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