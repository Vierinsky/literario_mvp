# Handoff para siguiente conversación
Documento hecho en: 06-05-2026
## Pendientes de producto, robustez, ingestión y expansión operativa

## Contexto del proyecto

`literario_mvp` es un proyecto Django orientado a construir un recomendador literario de fantasía y ciencia ficción, con foco en:

- descubrimiento por experiencia lectora
- catálogo curado
- aprendizaje progresivo de AI Engineering
- base futura para herramientas literarias conectadas con una marca autoral

## Importante

La siguiente conversación **no** debería enfocarse en embeddings reales ni búsqueda semántica vectorial, porque ya existe otro handoff específico para esa línea.

Esta nueva conversación debería enfocarse en:

- cerrar mejor el MVP funcional
- revisar lo pendiente respecto a los docs iniciales
- fortalecer ingestión de catálogo
- mejorar robustez operativa
- evaluar una línea tangente de scraping como fuente de datos

---

## Estado actual ya implementado

### Base web
- Proyecto Django levantado
- Settings separados por entorno:
  - `base.py`
  - `dev.py`
  - `prod.py`
- Templates globales
- Static files básicos
- Home, About y navegación base

### Apps creadas
- `core`
- `catalog`
- `recommendations`
- `tracking`
- `subscribers`
- `editorial`

### Catálogo
- Modelos:
  - `Author`
  - `Book`
  - `BookTag`
- `length_category` derivada desde `page_count`
- Admin funcional
- Mini-semilla cargada de forma manual/script

### Recomendación actual
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

### Tracking
- `SearchRequest`
- `SearchResult`
- `session_id` anónima
- Persistencia de búsquedas y resultados

### Subscribers
- `EmailSubscriber`
- Captura de email con consentimiento
- Asociación con `first_search_request`

### Editorial
- `EditorialPost`
- `EditorialPostBook`
- Índice y detalle público
- Se simplificó el modelo para usar un solo tipo de post editorial, sin `post_type`

### Capa semántica preparatoria
- Existe `embedding_text` en `Book`
- Existe builder explícito para construirlo
- Existe rebuild explícito por libro y masivo
- Existe management command:
  - `python manage.py rebuild_embedding_texts`

---

## Qué quedó pendiente respecto a los documentos iniciales

### 1. Base de datos
- El plan técnico proponía PostgreSQL
- Actualmente el proyecto sigue en SQLite
- Hay que evaluar cuándo conviene migrar y cómo hacerlo sin dolor

### 2. Ingestión de catálogo
- Los docs proponían una lista semilla más pipeline de enriquecimiento
- Actualmente la carga es manual/script local
- Falta una estrategia de ingestión más robusta y repetible

### 3. Enriquecimiento externo
- Aún no existe integración con Open Library u otra fuente estructurada
- Tampoco existe pipeline de normalización y validación más maduro

### 4. Newsletter real
- Existe captura de email
- No existe todavía integración con proveedor externo
- No existe todavía secuencia de bienvenida real

### 5. Robustez técnica
Faltan varias piezas sanas para una beta más seria:
- rate limiting
- validaciones más finas
- tests
- manejo de errores más robusto
- revisión de seguridad mínima
- observabilidad/logging algo más claro

### 6. Seed operativa
- Existe script de seed manual
- Falta formalizar mejor parte de la operación de carga

### 7. Revisión contra documentos
- Conviene hacer un cruce ordenado entre:
  - PRD
  - plan técnico
  - backlog
  - especificación de modelos
  - y lo realmente implementado

---

## Tema importante de esta siguiente conversación
# Ingestión de datos y scraping robusto

Además de revisar lo pendiente del MVP, se quiere explorar una posible línea de ingestión más robusta basada en scraping.

## Pregunta estratégica a responder

¿Qué fuente o fuentes de datos conviene usar para enriquecer el catálogo literario del proyecto, y cómo debería diseñarse un pipeline robusto de scraping / extracción / normalización?

## Posibles fuentes candidatas a evaluar

### Fuentes estructuradas / API / datasets
- Open Library
- Google Books API
- Wikipedia / Wikidata
- otras fuentes con metadata bibliográfica accesible

### Fuentes web con scraping
- Goodreads
- StoryGraph
- editoriales
- librerías online
- blogs curatoriales
- sitios especializados en ciencia ficción y fantasía

## Importante sobre esta línea

La idea no es decidir apresuradamente “hagamos scraper de Goodreads” solo porque sí.

La siguiente conversación debería evaluar:
- viabilidad técnica
- robustez
- legalidad / términos de uso
- estabilidad
- costo de mantenimiento
- valor real de la información extraída

---

## Posible proyecto tangente
# Scraper / ingestor literario

Puede evaluarse si esta línea conviene vivir como:

### Opción A
Parte del mismo repo `literario_mvp`

### Opción B
Proyecto aparte, por ejemplo:
- `literary_catalog_ingestion`
- `book_metadata_pipeline`
- `literary_scraper`

### Mi intuición actual
Si el scraping crece mucho, probablemente convenga separarlo como proyecto aparte o como módulo claramente desacoplado, porque mezcla preocupaciones distintas:

- recomendador web / producto
- extracción y limpieza de datos
- scraping y automatización
- posible enriquecimiento con IA

---

## Posible alcance de ese proyecto tangente

### Ingestión mínima
- extraer título, autor, sinopsis, páginas, serie, idioma, tags/géneros visibles

### Enriquecimiento
- unificar nombres
- limpiar texto
- normalizar géneros y tags
- identificar duplicados
- construir ficha canónica por libro

### Curaduría asistida
- dejar campos sugeridos para revisión humana
- eventualmente usar IA para:
  - resumir descripciones
  - sugerir tags curatoriales
  - detectar tono/ritmo/temática
  - normalizar textos ruidosos

### Salida esperada
- CSV limpio
- JSON limpio
- carga a DB
- o integración con modelos de Django

---

## Herramientas de scraping a evaluar en la siguiente conversación

### Selenium
Ventajas:
- útil para sitios con mucha interacción
- conocido y ampliamente usado

Desventajas:
- más pesado
- más lento
- menos elegante para scraping moderno

### Playwright
Ventajas:
- moderno
- robusto
- bueno para sitios dinámicos
- automatización sólida
- mejor opción general que Selenium en muchos casos

Desventajas:
- igual implica mantenimiento si el sitio cambia mucho

### Requests + BeautifulSoup
Ventajas:
- más simple
- más liviano
- ideal si el sitio es estático

Desventajas:
- se queda corto si hay JS fuerte o UI dinámica

### Scrapy
Ventajas:
- muy bueno para scraping serio a escala
- crawling, pipelines y estructura más robusta

Desventajas:
- curva de aprendizaje mayor
- quizá demasiado para fase temprana si todavía no se definió fuente real

## Intuición actual
Si se va a explorar scraping moderno y relativamente robusto, **Playwright** parece muy buena primera candidata.
Si la fuente final resultara ser mayormente estática y simple, entonces también convendría evaluar si Requests + BeautifulSoup bastan.

---

## Posible uso de IA en el proyecto tangente de ingestión

Sí, se puede evaluar una capa IA, pero no como humo.
La IA podría ser útil en tareas como:

- limpiar y resumir sinopsis muy largas
- sugerir tags curatoriales
- detectar tono / ritmo / temática
- comparar registros duplicados
- construir `embedding_text` preliminar
- normalizar metadata ruidosa

### Importante
No usar IA como reemplazo de toda la curaduría.
Usarla como apoyo para:
- acelerar
- sugerir
- limpiar
- priorizar revisión humana

---

## Preguntas clave que esa siguiente conversación debería responder

### Producto / roadmap
1. ¿Qué partes del PRD y del plan técnico siguen pendientes y cuáles valen más la pena abordar primero?
2. ¿Qué tan necesario es migrar ya a PostgreSQL?
3. ¿Qué robustez mínima conviene agregar antes de seguir creciendo?

### Ingestión
4. ¿Cuál debería ser la estrategia de ingestión del catálogo en la siguiente fase?
5. ¿Conviene seguir con seed manual mejorado, Open Library, scraping o una mezcla?
6. ¿Qué fuente externa vale más la pena por estabilidad y calidad?
7. ¿Conviene hacer el ingestor como parte del repo o como proyecto separado?

### Scraping
8. ¿Qué herramienta conviene evaluar primero: Playwright, Selenium, Requests/BS4 o Scrapy?
9. ¿Qué datos conviene extraer exactamente y cuáles no?
10. ¿Cómo normalizar y validar la información scrapeada?

### IA aplicada a ingestión
11. ¿Dónde sí tiene sentido usar IA dentro del pipeline de ingestión?
12. ¿Qué partes deberían seguir siendo humanas o explícitamente curadas?

---

## Prioridades sugeridas para esa conversación

### Prioridad alta
1. Revisar lo pendiente vs docs iniciales
2. Definir estrategia de ingestión futura
3. Evaluar fuente o combinación de fuentes
4. Decidir si scraping va dentro o fuera del repo principal
5. Evaluar robustez mínima faltante para el MVP

### Prioridad media
6. Diseñar pipeline de normalización de metadata
7. Evaluar IA asistida para curaduría/enriquecimiento
8. Formalizar mejor seed e ingestión operativa

### Prioridad posterior
9. Migración a PostgreSQL
10. Integración newsletter real
11. tests y mejoras de robustez más amplias

---

## Importante sobre estilo de explicación

El usuario quiere explicaciones claras y pedagógicas, especialmente cuando el tema se acerque a IA/AI Engineering.
No asumir demasiada familiaridad previa con:
- embeddings
- vectorización
- arquitectura de pipelines IA
- decisiones de diseño de sistemas de recomendación

También conviene explicar no solo qué hacer, sino por qué se hace así.

---

## Resultado ideal de esa siguiente conversación

Salir con algo como:

1. diagnóstico claro de qué falta del MVP respecto a los docs
2. roadmap de cierre del MVP funcional
3. estrategia de ingestión elegida
4. decisión sobre scraping:
   - sí / no
   - con qué herramienta
   - con qué alcance
5. posible diseño de pipeline o proyecto tangente de ingestión
6. backlog ejecutable de próximos pasos