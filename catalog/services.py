from catalog.models import Book, BookTag
from django.utils import timezone

REQUIRED_TAG_TYPES_FOR_RECOMMENDATION = {
    "tone_primary",
    "tone_secondary",
    "pace",
    "theme",
}

def humanize_genre(value):
    '''
    Convierte el género interno en una etiqueta legible.
    '''
    mapping = {
        "fantasy": "fantasía",
        "science_fiction": "ciencia ficción",
    }
    return mapping.get(value, value)


def humanize_length(value):
    """
    Convierte la categoría de longitud interna en una etiqueta legible.
    """
    mapping = {
        "short": "corta",
        "medium": "media",
        "long": "larga",
    }
    return mapping.get(value, value)


def humanize_tag_value(value):
    """
    Convierte valores internos de tags curatoriales en etiquetas legibles.
    """
    mapping = {
        "hopeful": "esperanzador",
        "melancholic": "melancólico",
        "dark": "oscuro",
        "unsettling": "inquietante",
        "strange": "extraño",
        "contemplative": "contemplativo",
        "balanced": "equilibrado",
        "fast": "ágil",
        "romantasy": "romantasy",
        "cozy": "cozy",
        "dystopia": "distopía",
        "horror": "horror",
        "space_opera": "space opera",
        "grimdark": "grimdark / dark fantasy",
        "cli_fi": "cli-fi / ficción climática",
        "political_intrigue": "intriga política",
        "mythic_reimagining": "mitología / reimaginación",
        "first_contact": "primer contacto alienígena",
        "epic": "épica",
    }
    return mapping.get(value, value)


def get_book_tag_values(book):
    """
    Retorna un diccionario simple con los valores curatoriales relevantes del libro.

    Parameters
    ----------
    book : Book
        Libro del catálogo.

    Returns
    -------
    dict
        Diccionario con claves curatoriales relevantes.
    """
    tag_map = {
        "tone_primary": "",
        "tone_secondary": "",
        "pace": "",
        "theme": [],
    }

    tags = BookTag.objects.filter(book=book)

    for tag in tags:
        if tag.tag_type == "tone_primary":
            tag_map["tone_primary"] = humanize_tag_value(tag.tag_value)
        elif tag.tag_type == "tone_secondary":
            tag_map["tone_secondary"] = humanize_tag_value(tag.tag_value)
        elif tag.tag_type == "pace":
            tag_map["pace"] = humanize_tag_value(tag.tag_value)
        elif tag.tag_type == "theme":
            tag_map["theme"].append(humanize_tag_value(tag.tag_value))

    return tag_map

def get_book_tag_types(book):
    """
    Obtiene los tipos de tags asociados a un libro.

    Parameters
    ----------
    book : Book
        Libro que se quiere revisar.

    Returns
    -------
    set[str]
        Conjunto con los tag_type presentes en el libro.
    """
    return set(
        BookTag.objects
        .filter(book=book)
        .values_list("tag_type", flat=True)
    )


def get_missing_required_tag_types(book):
    """
    Detecta qué tipos de tags mínimos faltan en un libro.

    Para el MVP, un libro listo para recomendación debería tener:
    - tone_primary
    - tone_secondary
    - pace
    - theme

    Parameters
    ----------
    book : Book
        Libro que se quiere validar.

    Returns
    -------
    set[str]
        Conjunto con los tag_type faltantes.
    """
    existing_tag_types = get_book_tag_types(book)

    return REQUIRED_TAG_TYPES_FOR_RECOMMENDATION - existing_tag_types


def get_catalog_quality_issues(book):
    """
    Detecta problemas básicos de calidad en la ficha de un libro.

    Esta función no modifica el libro. Solo informa qué falta o qué
    podría impedir que el libro sea usado correctamente en recomendaciones
    o preparación semántica futura.

    Parameters
    ----------
    book : Book
        Libro que se quiere validar.

    Returns
    -------
    list[str]
        Lista de problemas detectados.
    """
    issues = []

    if not book.title:
        issues.append("Falta título.")

    if not book.author_id:
        issues.append("Falta autor.")

    if not book.synopsis:
        issues.append("Falta sinopsis.")

    if not book.genre_main:
        issues.append("Falta género principal.")

    if not book.page_count and not book.length_category:
        issues.append("Falta page_count o length_category.")

    if not book.length_category:
        issues.append("Falta categoría de longitud.")

    missing_tag_types = get_missing_required_tag_types(book)

    for tag_type in sorted(missing_tag_types):
        issues.append(f"Falta tag requerido: {tag_type}.")

    return issues


def is_book_ready_for_recommendation(book):
    """
    Indica si un libro está listo para participar en recomendaciones.

    La regla combina:
    - interruptor is_active;
    - estado operativo del catálogo;
    - estado mínimo de metadata;
    - campos y tags curatoriales mínimos.

    Parameters
    ----------
    book : Book
        Libro que se quiere evaluar.

    Returns
    -------
    bool
        True si el libro está listo para recomendarse.
        False en caso contrario.
    """
    has_valid_catalog_status = (
        book.catalog_status == Book.CatalogStatusChoices.ACTIVE
    )

    has_valid_metadata_status = book.metadata_status in [
        Book.MetadataStatusChoices.PARTIAL,
        Book.MetadataStatusChoices.VALIDATED,
    ]

    has_no_quality_issues = not get_catalog_quality_issues(book)

    return all([
        book.is_active,
        has_valid_catalog_status,
        has_valid_metadata_status,
        has_no_quality_issues,
    ])


def is_book_ready_for_embedding_text(book):
    """
    Indica si un libro está listo para construir o reconstruir embedding_text.

    Ojo: esto NO genera embeddings reales. Solo valida si el libro tiene
    metadata suficiente para armar una representación textual útil.

    Parameters
    ----------
    book : Book
        Libro que se quiere evaluar.

    Returns
    -------
    bool
        True si el libro está listo para construir embedding_text.
        False en caso contrario.
    """
    return is_book_ready_for_recommendation(book)


def get_books_ready_for_embedding_text():
    """
    Retorna libros candidatos a construir o reconstruir embedding_text.

    Esta función aplica primero filtros de base de datos para reducir el
    universo de libros. Las validaciones finas de tags y campos pueden
    hacerse luego con is_book_ready_for_embedding_text(book).

    Returns
    -------
    QuerySet[Book]
        QuerySet con libros activos y metadata mínimamente utilizable.
    """
    return (
        Book.objects.filter(
            is_active=True,
            catalog_status=Book.CatalogStatusChoices.ACTIVE,
            metadata_status__in=[
                Book.MetadataStatusChoices.PARTIAL,
                Book.MetadataStatusChoices.VALIDATED,
            ],
        )
        .select_related("author")
        .prefetch_related("tags")
    )


def get_recommendable_books_queryset():
    """
    Retorna el queryset base de libros aptos para recomendación.

    Un libro se considera apto si:
    - está activo;
    - fue aprobado para el catálogo;
    - tiene metadata parcial o validada.

    Returns
    -------
    QuerySet[Book]
        QuerySet optimizado con author y tags precargados.
    """
    return (
        Book.objects.filter(
            is_active=True,
            catalog_status=Book.CatalogStatusChoices.ACTIVE,
            metadata_status__in=[
                Book.MetadataStatusChoices.PARTIAL,
                Book.MetadataStatusChoices.VALIDATED,
            ],
        )
        .select_related("author")
        .prefetch_related("tags")
    )


def build_embedding_text(book):
    """
    Construye el embedding_text de un libro a partir de su metadata principal
    y de sus tags curatoriales.

    Parameters
    ----------
    book : Book
        Libro del catálogo.

    Returns
    -------
    str
        Texto enriquecido y consistente para futuras tareas semánticas.
    """
    tag_map = get_book_tag_values(book)

    lines = [
        f"Título: {book.title}.",
        f"Autor: {book.author.name}.",
        f"Género: {humanize_genre(book.genre_main)}.",
    ]

    if book.synopsis:
        lines.append(f"Sinopsis: {book.synopsis}")

    if tag_map["tone_primary"]:
        lines.append(f"Tono principal: {tag_map['tone_primary']}.")

    if tag_map["tone_secondary"]:
        lines.append(f"Tono secundario: {tag_map['tone_secondary']}.")

    if tag_map["pace"]:
        lines.append(f"Ritmo: {tag_map['pace']}.")

    if tag_map["theme"]:
        lines.append(f"Temática: {', '.join(tag_map['theme'])}.")

    if book.length_category:
        lines.append(f"Longitud: {humanize_length(book.length_category)}.")

    lines.append(
        f"Disponible en español: {'sí' if book.available_in_spanish else 'no'}."
    )

    return "\n".join(lines)

def update_book_embedding_text(book):
    """
    Construye y guarda el embedding_text de un libro.

    Parameters
    ----------
    book : Book
        Libro del catálogo.

    Returns
    -------
    Book
        Libro actualizado.
    """
    embedding_text = build_embedding_text(book)

    Book.objects.filter(pk=book.pk).update(
        embedding_text=embedding_text,
        updated_at=timezone.now()
    )

    book.refresh_from_db()
    return book

def rebuild_all_embedding_texts(only_ready=True):
    """
    Regenera el embedding_text de los libros del catálogo.

    Parameters
    ----------
    only_ready : bool
        Si es True, regenera solo libros activos con metadata mínima usable.
        Si es False, regenera todos los libros del catálogo.

    Returns
    -------
    int
        Cantidad de libros actualizados.
    """
    if only_ready:
        books = get_books_ready_for_embedding_text()
    else:
        books = (
            Book.objects
            .select_related("author")
            .prefetch_related("tags")
            .all()
        )

    count = 0

    for book in books:
        if only_ready and not is_book_ready_for_embedding_text(book):
            continue

        update_book_embedding_text(book)
        count += 1

    return count
