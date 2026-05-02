from catalog.models import Book

def humanize_value(value):
    """
    Convierte valores internos del sistema en etiquetas legibles.
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
        "short": "corta",
        "medium": "media",
        "long": "larga",
    }
    return mapping.get(value, value)

def build_match_explanation(book, cleaned_data):
    """
    Construye una explicación breve y controlada para un libro recomendado.

    Parameters
    ----------
    book : Book
        Libro recomendado.
    cleaned_data : dict
        Datos validados del formulario.

    Returns
    -------
    str
        Explicación breve del match.
    """
    fragments = []

    tone = cleaned_data.get("tone")
    pace = cleaned_data.get("pace")
    theme = cleaned_data.get("theme")
    length = cleaned_data.get("length")

    if tone:
        fragments.append(f"un tono {humanize_value(tone)}")

    if pace:
        fragments.append(f"un ritmo {humanize_value(pace)}")

    if theme:
        fragments.append(f"una veta de {humanize_value(theme)}")

    if length:
        fragments.append(f"una longitud {humanize_value(length)}")

    if fragments:
        joined = ", ".join(fragments[:-1])
        if len(fragments) > 1:
            joined = f"{joined} y {fragments[-1]}" if joined else fragments[-1]
        else:
            joined = fragments[0]

        return f"Te lo recomendé porque encaja con {joined}."

    return "Te lo recomendé porque encaja razonablemente con los filtros seleccionados."


def get_filtered_books(cleaned_data):
    """
    Retorna hasta 3 libros activos filtrados por tags curatoriales básicos
    y los enriquece con una explicación de match.

    Parameters
    ----------
    cleaned_data : dict
        Datos validados del formulario.

    Returns
    -------
    list[dict]
        Lista de resultados enriquecidos.
    """
    books = (
        Book.objects.filter(is_active=True)
        .select_related("author")
        .prefetch_related("tags")
    )

    tone = cleaned_data.get("tone")
    pace = cleaned_data.get("pace")
    theme = cleaned_data.get("theme")
    length = cleaned_data.get("length")
    include_english = cleaned_data.get("include_english")

    if tone:
        books = books.filter(
            tags__tag_type__in=["tone_primary", "tone_secondary"],
            tags__tag_value=tone,
        )

    if pace:
        books = books.filter(
            tags__tag_type="pace",
            tags__tag_value=pace,
        )

    if theme:
        books = books.filter(
            tags__tag_type="theme",
            tags__tag_value=theme,
        )

    if length:
        books = books.filter(length_category=length)

    if not include_english:
        books = books.filter(available_in_spanish=True)

    books = books.distinct().order_by("title")[:3]

    enriched_results = []
    for book in books:
        enriched_results.append(
            {
                "book": book,
                "match_explanation": build_match_explanation(book, cleaned_data),
            }
        )

    return enriched_results