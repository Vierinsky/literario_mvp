from django.shortcuts import render

from catalog.models import Book
from .forms import BookSearchForm
from tracking.models import SearchRequest, SearchResult

import hashlib
import uuid


def _get_or_create_session_id(request):
    """
    Obtiene una session_id anónima persistida en la sesión de Django.
    """
    session_id = request.session.get("literario_session_id")

    if not session_id:
        session_id = uuid.uuid4().hex
        request.session["literario_session_id"] = session_id

    return session_id


def _hash_value(raw_value):
    """
    Devuelve un hash SHA-256 de un valor de texto.
    """
    if not raw_value:
        return ""

    return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()


def _persist_search(request, cleaned_data, results):
    """
    Guarda la búsqueda y los resultados mostrados.
    """
    session_id = _get_or_create_session_id(request)

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
        user_agent_hash=_hash_value(user_agent),
        ip_hash=_hash_value(remote_addr),
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


def _humanize_value(value):
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

def _build_match_explanation(book, cleaned_data):
    """
    Construye una explicación breve y controlada para un libro recomendado.
    """
    fragments = []

    tone = cleaned_data.get("tone")
    pace = cleaned_data.get("pace")
    theme = cleaned_data.get("theme")
    length = cleaned_data.get("length")

    if tone:
        fragments.append(f"un tono {_humanize_value(tone)}")

    if pace:
        fragments.append(f"un ritmo {_humanize_value(pace)}")

    if theme:
        fragments.append(f"una veta de {_humanize_value(theme)}")

    if length:
        fragments.append(f"una longitud {_humanize_value(length)}")

    if fragments:
        joined = ", ".join(fragments[:-1])
        if len(fragments) > 1:
            joined = f"{joined} y {fragments[-1]}" if joined else fragments[-1]
        else:
            joined = fragments[0]

        return f"Te lo recomendé porque encaja con {joined}."
    
    return "Te lo recomendé porque encaja razonablemente con los filtros seleccionados."

def _get_filtered_books(cleaned_data):
    '''
    Retorna hasta 3 libros activos filtrados por tags curatoriales básicos.

    Parameters
    ----------
    cleaned_data : dict
        Datos validados del formulario.

    Returns
    -------
    QuerySet
        QuerySet de libros filtrados.
    '''
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
        books = books.filter(tags__tag_type__in=["tone_primary", "tone_secondary"], tags__tag_value=tone)

    if pace:
        books = books.filter(tags__tag_type="pace", tags__tag_value=pace)

    if theme:
        books = books.filter(tags__tag_type="theme", tags__tag_value=theme)

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
                "match_explanation": _build_match_explanation(book, cleaned_data),
            }
        )

    return enriched_results

def home(request):
    '''
    Renderiza la página de inicio del proyecto.
    '''
    form = BookSearchForm()

    context = {
        "form": form,
    }

    return render(request, "core/home.html", context)


def about(request):
    '''
    Renderiza la página sobre el proyecto.
    '''
    return render(request, "core/about.html")


def search_results(request):
    '''
    Renderiza una página de resultados inicial que muestra
    los datos enviados por el formulario y persiste la búsqueda
    en tracking.
    '''
    form = BookSearchForm(request.GET or None)

    context = {
        "form": form,
        "submitted_data": None,
        "results": [],
    }

    if form.is_valid():
        cleaned_data = form.cleaned_data
        results = _get_filtered_books(cleaned_data)

        context["submitted_data"] = cleaned_data
        context["results"] = results

        _persist_search(request, cleaned_data, results)

    return render(request, "core/search_results.html", context)