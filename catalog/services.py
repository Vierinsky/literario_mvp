from catalog.models import BookTag

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
    book.embedding_text = build_embedding_text(book)
    book.save(update_fields=["embedding_text", "updated_at"])
    return book

def rebuild_all_embedding_texts():
    """
    Regenera el embedding_text de todos los libros del catálogo.

    Returns
    -------
    int
        Cantidad de libros actualizados.
    """
    from catalog.models import Book

    books = Book.objects.select_related("author").prefetch_related("tags").all()

    count = 0
    for book in books:
        update_book_embedding_text(book)
        count += 1

    return count