import hashlib
import uuid

from .models import SearchRequest, SearchResult


def get_or_create_session_id(request):
    """
    Obtiene una session_id anónima persistida en la sesión de Django.

    Parameters
    ----------
    request : HttpRequest
        Request actual.

    Returns
    -------
    str
        Identificador de sesión anónima.
    """
    session_id = request.session.get("literario_session_id")

    if not session_id:
        session_id = uuid.uuid4().hex
        request.session["literario_session_id"] = session_id

    return session_id


def hash_value(raw_value):
    """
    Devuelve un hash SHA-256 de un valor de texto.

    Parameters
    ----------
    raw_value : str
        Valor de entrada a hashear.

    Returns
    -------
    str
        Hash SHA-256 en formato hexadecimal.
    """
    if not raw_value:
        return ""

    return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()


def persist_search(request, cleaned_data, results):
    """
    Guarda la búsqueda realizada y los resultados mostrados al usuario.

    Parameters
    ----------
    request : HttpRequest
        Request actual.
    cleaned_data : dict
        Datos validados del formulario de búsqueda.
    results : list[dict]
        Resultados enriquecidos devueltos por recommendations.

    Returns
    -------
    SearchRequest
        Objeto de búsqueda persistido.
    """
    session_id = get_or_create_session_id(request)

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    remote_addr = request.META.get("REMOTE_ADDR", "")

    search_request = SearchRequest.objects.create(
        session_id=session_id,
        query_text=cleaned_data.get("query_text", ""),
        tone_filter=cleaned_data.get("tone", ""),
        pace_filter=cleaned_data.get("pace", ""),
        theme_filter=cleaned_data.get("theme", ""),
        length_filter=cleaned_data.get("length", ""),
        include_english=cleaned_data.get("include_english", False),
        user_agent_hash=hash_value(user_agent),
        ip_hash=hash_value(remote_addr),
    )

    for index, result in enumerate(results, start=1):
        SearchResult.objects.create(
            search_request=search_request,
            book=result["book"],
            rank_position=index,
            match_explanation=result["match_explanation"],
            shown_to_user=True,
            clicked=False,
        )

    return search_request