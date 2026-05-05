import unicodedata

from django.db.models import Q

from catalog.models import Book


def normalize_text(text):
    """
    Normaliza un texto para comparación básica:
    - minúsculas
    - sin tildes
    - sin espacios sobrantes
    """
    if not text:
        return ""
    
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return text


def expand_query_terms(query_text):
    """
    Expande términos del usuario hacia equivalencias internas útiles
    para mejorar la búsqueda textual del MVP.

    Parameters
    ----------
    query_text : str
        Texto libre ingresado por el usuario.

    Returns
    -------
    list[str]
        Lista de términos normalizados y expandidos.
    """
    synonym_map = {
        "melancolico": ["melancholic"],
        "melancolica": ["melancholic"],
        "melancolia": ["melancholic"],
        "extrano": ["strange"],
        "extrana": ["strange"],
        "raro": ["strange"],
        "rara": ["strange"],
        "oscuro": ["dark"],
        "oscura": ["dark"],
        "inquietante": ["unsettling"],
        "lento": ["contemplative"],
        "lenta": ["contemplative"],
        "contemplativo": ["contemplative"],
        "contemplativa": ["contemplative"],
        "agil": ["fast"],
        "rapido": ["fast"],
        "romantasy": ["romantasy"],
        "cozy": ["cozy"],
        "distopia": ["dystopia"],
        "horror": ["horror"],
        "politica": ["political_intrigue"],
        "mitologia": ["mythic_reimagining"],
        "reimaginacion": ["mythic_reimagining"],
        "alienigena": ["first_contact"],
        "contacto": ["first_contact"],
        "corto": ["short"],
        "corta": ["short"],
        "medio": ["medium"],
        "media": ["medium"],
        "largo": ["long"],
        "larga": ["long"],
        "epic": ["epic"],
        "epico": ["epic"],
        "epica": ["epic"],
        "epopeya": ["epic"],
    }

    normalized_query = normalize_text(query_text)
    raw_terms = [term for term in normalized_query.split() if term]

    expanded_terms = []

    for term in raw_terms:
        expanded_terms.append(term)

        mapped_terms = synonym_map.get(term, [])
        expanded_terms.extend(mapped_terms)

    # quitamos duplicados preservando orden
    unique_terms = list(dict.fromkeys(expanded_terms))
    return unique_terms

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

    query_text = cleaned_data.get("query_text")
    tone = cleaned_data.get("tone")
    pace = cleaned_data.get("pace")
    theme = cleaned_data.get("theme")
    length = cleaned_data.get("length")

    if query_text:
        fragments.append("lo que escribiste en tu búsqueda")

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


def get_book_tag_map(book):
    """
    Retorna un diccionario simple con los tags del libro agrupados por tipo.
    """
    tag_map = {
        "tone_primary": [],
        "tone_secondary": [],
        "pace": [],
        "theme": [],
    }

    for tag in book.tags.all():
        if tag.tag_type in tag_map:
            tag_map[tag.tag_type].append(tag.tag_value)

    return tag_map


def score_book(book, cleaned_data, expanded_terms):
    """
    Calcula un puntaje simple de relevancia para un libro.

    Reglas iniciales:
    - coincidencia textual en título: +3
    - coincidencia textual en autor: +2
    - coincidencia textual en sinopsis: +1 por término
    - coincidencia textual en tags: +3 por término
    - coincidencia con tone: +4
    - coincidencia con pace: +3
    - coincidencia con theme: +4
    - coincidencia con length: +2
    """
    score = 0

    title_text = normalize_text(book.title)
    author_text = normalize_text(book.author.name)
    synopsis_text = normalize_text(book.synopsis or "")
    tag_map = get_book_tag_map(book)
    all_tag_values = []
    for values in tag_map.values():
        all_tag_values.extend(values)

    normalized_tag_values = [normalize_text(value) for value in all_tag_values]

    for term in expanded_terms:
        if term in title_text:
            score += 3

        if term in author_text:
            score += 2

        if term in synopsis_text:
            score += 1

        if any(term in tag_value for tag_value in normalized_tag_values):
            score += 3

    tone = cleaned_data.get("tone")
    pace = cleaned_data.get("pace")
    theme = cleaned_data.get("theme")
    length = cleaned_data.get("length")

    if tone and (tone in tag_map["tone_primary"] or tone in tag_map["tone_secondary"]):
        score += 4

    if pace and pace in tag_map["pace"]:
        score += 3

    if theme and theme in tag_map["theme"]:
        score += 4

    if length and book.length_category == length:
        score += 2

    return score


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

    query_text = cleaned_data.get("query_text", "").strip()
    tone = cleaned_data.get("tone")
    pace = cleaned_data.get("pace")
    theme = cleaned_data.get("theme")
    length = cleaned_data.get("length")
    include_english = cleaned_data.get("include_english")

    expanded_terms = []
    if query_text:
        expanded_terms = expand_query_terms(query_text)

        if expanded_terms:
            text_query = Q()

            for term in expanded_terms:
                text_query |= Q(title__icontains=term)
                text_query |= Q(synopsis__icontains=term)
                text_query |= Q(author__name__icontains=term)
                text_query |= Q(tags__tag_value__icontains=term)

                # Ojo:
                # Esto usa OR entre términos.
                # Eso significa que si encuentra coincidencia con cualquiera de las palabras, el libro puede entrar.
                # Para un catálogo chico, eso está bien como primer paso.

            books = books.filter(text_query)

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

    books = books.distinct()

    scored_results = []
    for book in books:
        score = score_book(book, cleaned_data, expanded_terms)
        scored_results.append(
            {
                "book": book,
                "score": score,
                "match_explanation": build_match_explanation(book, cleaned_data),
            }
        )
    
    scored_results.sort(key=lambda item: (-item["score"], item["book"].title))
    

    return scored_results[:3]
