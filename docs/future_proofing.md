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
6. implementación de modelo IA

La idea no es sobreconstruir desde el inicio, sino crecer por capas manteniendo una base ordenada.