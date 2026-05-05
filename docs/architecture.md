# Arquitectura actual

## Resumen

El proyecto está organizado en apps Django separadas por responsabilidad.

## Apps

### core
Responsable de:
- home
- about
- resultados
- integración del flujo principal entre formulario, resultados y captura de email

### catalog
Responsable de:
- `Author`
- `Book`
- `BookTag`

### recommendations
Responsable de:
- normalización de `query_text`
- expansión de términos
- filtrado de libros
- scoring y ranking simple
- construcción de explicación breve

### tracking
Responsable de:
- `SearchRequest`
- `SearchResult`
- persistencia de búsquedas
- session_id anónima

### subscribers
Responsable de:
- `EmailSubscriber`
- formulario de captura de email
- consentimiento
- asociación inicial con `first_search_request`

### editorial
Responsable de:
- `EditorialPost`
- `EditorialPostBook`
- índice y detalle editorial

## Flujo principal actual

1. El usuario entra a la home
2. Completa texto libre y/o filtros
3. `core.views.search_results` valida el formulario
4. `recommendations.services.get_filtered_books()` devuelve resultados enriquecidos
5. `tracking.services.persist_search()` guarda búsqueda y resultados
6. Se renderiza la página de resultados
7. El usuario puede dejar su email
8. `subscribers.views.subscribe_email()` guarda el suscriptor y lo asocia a la búsqueda

## Base de datos actual

Por ahora se usa SQLite.
Más adelante se planea migrar a PostgreSQL.