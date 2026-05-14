import requests
import unicodedata

OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"

def search_openlibrary_book(title, author=None, limit=5, search_mode="structured"):
    """
    Busca libros en Open Library usando título y, opcionalmente, autor.

    Permite dos modos de búsqueda:
    - structured: usa parámetros title y author.
    - free: usa q con título + autor.

    Parameters
    ----------
    title : str
        Título del libro a buscar.

    author : str, optional
        Nombre del autor. Ayuda a reducir falsos positivos.

    limit : int
        Cantidad máxima de resultados a solicitar.

    search_mode : str
        Modo de búsqueda. Puede ser 'structured' o 'free'.

    Returns
    -------
    dict
        Respuesta JSON cruda entregada por Open Library.

    Raises
    ------
    requests.RequestException
        Si ocurre un error de red, timeout o respuesta HTTP inválida.
    """
    fields = ",".join([
        "key",
        "title",
        "author_name",
        "author_key",
        "first_publish_year",
        "edition_count",
        "isbn",
        "language",
        "cover_i",
        "subject",
    ])

    if search_mode == "structured":

        params = {
            "title": title,
            "limit": limit,
            "fields": fields,
            }
    
        if author:
            params["author"] = author

    elif search_mode == "free":
        query_parts = [title]

        if author:
            query_parts.append(author)

            params = {
                "q": " ".join(query_parts),
                "limit": limit,
                "fields": fields,
            }

        else:
            raise ValueError(
                "search_mode debe ser 'structured' o 'free'."
            )

    response = requests.get(
        OPEN_LIBRARY_SEARCH_URL,
        params=params,
        timeout=20,
    )
    
    response.raise_for_status()
    return response.json()
    

def normalize_text_for_matching(text):
    """
    Normaliza texto para comparar títulos y autores.

    La normalización elimina tildes, pasa a minúsculas y limpia espacios.
    Esto ayuda a comparar entradas como 'El Hobbit', 'Hobbit' o nombres
    de autores con variaciones menores.

    Parameters
    ----------
    text : str
        Texto a normalizar.

    Returns
    -------
    str
        Texto normalizado.
    """
    if not text:
        return ""
    
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    return " ".join(text.split())


def score_openlibrary_candidate(candidate, expected_title, expected_author=None):
    """
    Calcula un score simple para ordenar candidatos de Open Library.

    Este score no decide todavía qué importar. Solo ayuda a mostrar primero
    los candidatos más probables.

    Parameters
    ----------
    candidate : dict
        Candidato normalizado desde Open Library.

    expected_title : str
        Título buscado originalmente.

    expected_author : str, optional
        Autor esperado.

    Returns
    -------
    int
        Puntaje de coincidencia. A mayor puntaje, mejor candidato.
    """
    score = 0

    candidate_title = normalize_text_for_matching(candidate.get("title", ""))
    expected_title_norm = normalize_text_for_matching(expected_title)

    candidate_author = normalize_text_for_matching(
        candidate.get("author_name", "")
    )
    expected_author_norm = normalize_text_for_matching(expected_author or "")

    # Coincidencia exacta o parcial de título.
    if candidate_title == expected_title_norm:
        score += 10
    elif expected_title_norm in candidate_title:
        score += 6
    elif candidate_title in expected_title_norm:
        score += 4

    # Coincidencia de autor.
    if expected_author_norm:
        if candidate_author == expected_author_norm:
            score += 10
        elif expected_author_norm in candidate_author:
            score += 6
        elif candidate_author in expected_author_norm:
            score += 4

    # Preferimos obras con año de primera publicación.
    if candidate.get("publication_year"):
        score += 2

    # Preferimos candidatos con portada.
    if candidate.get("cover_url"):
        score += 1

    # Penalizamos títulos que suelen indicar material secundario.
    suspicious_terms = [
        "study guide",
        "summary",
        "analysis",
        "companion",
        "sparknotes",
        "supersummary",
        "graphic novel",
    ]

    if any(term in candidate_title for term in suspicious_terms):
        score -= 8

    return score


def normalize_openlibrary_result(raw_doc):
    """
    Normaliza un resultado individual de Open Library a un formato interno.

    Parameters
    ----------
    raw_doc : dict
        Documento individual dentro de la clave 'docs' de Open Library.

    Returns
    -------
    dict
        Metadata normalizada para revisión o importación posterior.
    """
    author_names = raw_doc.get("author_name") or []
    isbn_values = raw_doc.get("isbn") or []
    languages = raw_doc.get("language") or []
    subjects = raw_doc.get("subject") or []

    cover_id = raw_doc.get("cover_i")
    cover_url = ""

    if cover_id:
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

    return {
        "source": "openlibrary",
        "external_openlibrary_id": raw_doc.get("key", ""),
        "title": raw_doc.get("title", ""),
        "author_name": author_names[0] if author_names else "",
        "publication_year": raw_doc.get("first_publish_year"),
        "isbn": isbn_values[0] if isbn_values else "",
        "original_language": languages[0] if languages else "",
        "cover_url": cover_url,
        "subjects": subjects[:20],
        "raw": raw_doc,
    }

def get_openlibrary_candidates(title, author=None, limit=5):
    """
    Busca, normaliza y ordena candidatos de libros desde Open Library.

    Primero intenta una búsqueda estructurada por título y autor.
    Si no encuentra resultados, usa una búsqueda libre con q.

    Parameters
    ----------
    title : str
        Título del libro buscado.

    author : str, optional
        Autor esperado.

    limit : int
        Cantidad máxima de candidatos a retornar.

    Returns
    -------
    list[dict]
        Lista de candidatos normalizados y ordenados por score interno.

    Raises
    ------
    requests.RequestException
        Si ambas búsquedas fallan por error de red o HTTP.
    """
    raw_response = search_openlibrary_book(
        title=title,
        author=author,
        limit=limit,
    )

    docs = raw_response.get("docs", [])

    candidates = [
        normalize_openlibrary_result(doc)
        for doc in docs
    ]

    for candidate in candidates:
        candidate["match_score"] = score_openlibrary_candidate(
            candidate=candidate,
            expected_title=title,
            expected_author=author,
        )

    candidates.sort(
        key=lambda item: (
            -item["match_score"],
            item.get("title", ""),
        )
    )

    return candidates

