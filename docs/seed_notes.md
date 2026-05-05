# Notas sobre la seed actual

## Carga manual inicial

La mini-semilla actual se cargó mediante:

```text
scripts/load_seed_books.py
```

## Libros actualmente cargados
- Un mago de Terramar
- El nombre del viento
- Nacidos de la bruma: El imperio final
- La voz de las espadas
- La mano izquierda de la oscuridad
- Aniquilación

## Criterio de carga

Cada libro incluye:

- autor
- sinopsis breve útil para búsqueda
- género principal
- page_count
- length_category derivada
- tags mínimos:
    - tone_primary
    - tone_secondary
    - pace
    - theme

## Convención de tags

Los tag_value se guardan con valores internos consistentes, por ejemplo:

- melancholic
- strange
- contemplative
- political_intrigue
- mythic_reimagining
- horror