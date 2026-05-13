import requests

OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"

def search_openlibrary_book(title, author=None, limit=5):
    """
    Busca libros en Open Library usando título y, opcionalmente, autor.

    Esta función consulta la Search API de Open Library y retorna la
    respuesta JSON cruda. No escribe en la base de datos.

    Parameters
    ----------
    title : str
        Título del libro a buscar.

    author : str, optional
        Nombre del autor. Ayuda a reducir falsos positivos.

    limit : int
        Cantidad máxima de resultados a solicitar.

    Returns
    -------
    dict
        Respuesta JSON cruda entregada por Open Library.

    Raises
    ------
    requests.HTTPError
        Si la API responde con un error HTTP.
    """
    query_parts = [title]

    if author:
        query_parts.append(author)

        params = {
        "q": " ".join(query_parts),
        "limit": limit,
        "fields": ",".join([
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
        ]),
        }

        response = requests.get(
            OPEN_LIBRARY_SEARCH_URL,
            params=params,
            timeout=15,
        )
        
        response.raise_for_status()
        return response.json()
    

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
    Busca y normaliza candidatos de libros desde Open Library.

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
        Lista de candidatos normalizados.
    """
    raw_response = search_openlibrary_book(
        title=title,
        author=author,
        limit=limit,
    )

    docs = raw_response.get("docs", [])

    return [
        normalize_openlibrary_result(doc)
        for doc in docs
    ]

