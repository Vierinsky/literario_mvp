import hashlib
import uuid

from django.shortcuts import render

from recommendations.services import get_filtered_books
from subscribers.forms import EmailCaptureForm
from tracking.models import SearchRequest, SearchResult

from .forms import BookSearchForm


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
        "email_form": EmailCaptureForm,
    }

    if form.is_valid():
        cleaned_data = form.cleaned_data
        results = get_filtered_books(cleaned_data)
        search_request = _persist_search(request, cleaned_data, results)

        context["submitted_data"] = cleaned_data
        context["results"] = results
        context["email_form"] = EmailCaptureForm(
            initial={"search_request_id": search_request.id}
        )

        # _persist_search(request, cleaned_data, results)

    return render(request, "core/search_results.html", context)
