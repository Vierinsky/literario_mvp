# AI roadmap

## Propósito

Este proyecto busca servir como base web y de datos para aprender AI Engineering aplicado a recomendación literaria.

## Estado actual

Actualmente el sistema usa:
- búsqueda textual básica
- filtros curatoriales
- normalización simple de términos
- ranking heurístico
- explicaciones controladas

## Próxima capa de IA

### 1. Embedding text
Construir un texto enriquecido por libro combinando:
- título
- autor
- sinopsis
- género
- tono
- ritmo
- temática
- longitud

### 2. Embeddings
Generar embeddings para cada libro del catálogo.

### 3. Búsqueda semántica
Transformar la búsqueda del usuario en embedding y compararla con el catálogo.

### 4. Ranking híbrido
Combinar:
- similitud semántica
- filtros explícitos
- tags curatoriales
- disponibilidad en español
- longitud
- score editorial

## Mejores posteriores

- reranking
- mejores explicaciones
- enriquecimiento asistido por IA
- segmentación por comportamiento