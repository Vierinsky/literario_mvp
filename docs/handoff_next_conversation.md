# Handoff para siguiente conversación
Documento hecho en: 06-05-2026
## Proyecto

`literario_mvp`

Proyecto Django para explorar un recomendador literario de fantasía y ciencia ficción, con foco en:
- descubrimiento por experiencia lectora,
- catálogo curado,
- aprendizaje progresivo de AI Engineering,
- y base futura para herramientas literarias conectadas con una marca autoral.

---

## Objetivo de esta fase ya cubierta

En esta conversación se construyó la base funcional del MVP web y una primera capa de inteligencia no-vectorial.

### Ya implementado

#### Base web
- Proyecto Django levantado
- Settings separados por entorno:
  - `base.py`
  - `dev.py`
  - `prod.py`
- Templates globales
- Static files básicos
- Home, About y navegación base

#### Apps creadas
- `core`
- `catalog`
- `recommendations`
- `tracking`
- `subscribers`
- `editorial`

#### Catálogo
- Modelos:
  - `Author`
  - `Book`
  - `BookTag`
- `length_category` derivada desde `page_count`
- Admin funcional
- Mini-semilla cargada de forma manual/script

#### Recomendación
- Formulario de búsqueda con:
  - `query_text`
  - `tone`
  - `pace`
  - `length`
  - `theme`
  - `include_english`
- Búsqueda textual básica
- Normalización simple de términos
- Expansión de sinónimos básicos
- Ranking heurístico por score
- Explicación breve por resultado

#### Tracking
- `SearchRequest`
- `SearchResult`
- `session_id` anónima
- Persistencia de búsquedas y resultados

#### Subscribers
- `EmailSubscriber`
- Captura de email con consentimiento
- Asociación con `first_search_request`

#### Editorial
- `EditorialPost`
- `EditorialPostBook`
- Índice y detalle público
- Se simplificó el modelo para usar un solo tipo de post editorial, sin `post_type`

#### Capa IA inicial
- Se agregó `embedding_text` a `Book`
- Se diseñó y construyó una representación textual enriquecida por libro
- Se decidió explícitamente:
  - usar valores humanizados en `embedding_text`
  - no generarlo automáticamente en `save()`
  - regenerarlo con funciones explícitas

#### Servicios y arquitectura
- `recommendations/services.py`
- `tracking/services.py`
- `catalog/services.py`

#### Operación
- Existe management command:
  - `python manage.py rebuild_embedding_texts`

---

## Estado actual del proyecto

El proyecto ya permite:

1. buscar libros desde la home
2. usar filtros editoriales
3. obtener resultados con score y explicación
4. registrar la búsqueda
5. capturar email
6. asociar el email con la búsqueda
7. navegar una sección editorial mínima
8. regenerar `embedding_text` del catálogo

---

## Seed actual cargada

Actualmente hay al menos estos libros cargados:

- Un mago de Terramar
- El nombre del viento
- Nacidos de la bruma: El imperio final
- La voz de las espadas
- La mano izquierda de la oscuridad
- Aniquilación

Cada uno debería tener:
- sinopsis
- `page_count`
- `length_category`
- tags curatoriales mínimos:
  - `tone_primary`
  - `tone_secondary`
  - `pace`
  - `theme`

---

## Decisiones importantes tomadas

### 1. `embedding_text` antes de embeddings reales
Se decidió construir primero una buena representación textual del libro antes de pasar a vectores.

### 2. `embedding_text` no se recalcula automáticamente en `Book.save()`
Motivo:
- depende también de `BookTag`
- se prefirió regeneración explícita para mantener control y evitar magia oculta

### 3. Valores humanizados en `embedding_text`
Se decidió usar texto natural:
- `melancólico`
- `extraño`
- `mitología / reimaginación`

en lugar de claves internas tipo:
- `melancholic`
- `strange`
- `mythic_reimagining`

### 4. Simplificación editorial
Se eliminó `post_type` y se dejó un solo tipo de pieza editorial.

### 5. Priorización AI Engineering
Se decidió que el siguiente gran salto no sea más web base, sino embeddings reales y búsqueda semántica.

## Comando útil reciente

```powershell
python manage.py rebuild_embedding_texts
```

---

## Siguiente paso recomendado

### Tema principal de la siguiente conversación
**Embeddings reales y búsqueda semántica híbrida**

### Orden sugerido
1. revisar `embedding_text` de varios libros
2. definir estrategia de embeddings:
   - proveedor/modelo
   - dónde guardar vectores
3. generar embeddings del catálogo
4. construir comparación semántica entre query del usuario y libros
5. combinar:
   - score semántico
   - filtros explícitos
   - metadata curada
6. evaluar cómo persistir o recalcular embeddings

---

## Notas pedagógicas importantes

El usuario quiere que, en todo lo relacionado con IA/AI Engineering:
- las explicaciones sean especialmente pedagógicas,
- se explique qué se hace y por qué,
- y no se asuman conocimientos previos fuertes.

En particular:
- se pidió explicar desde cero qué es un embedding,
- por qué existe `embedding_text`,
- y por qué ciertas decisiones se tomaron así.

---

## Posibles temas secundarios para después

- formalizar mejor el seed como management command
- preparar `embedding_text_version` o `embedding_status`
- mejorar score/ranking
- migrar a PostgreSQL
- integrar proveedor real de email/newsletter
- ampliar catálogo
- tests básicos