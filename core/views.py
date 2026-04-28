from django.shortcuts import render

from catalog.models import Book
from .forms import BookSearchForm


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

    return books.distinct().order_by("title")[:3]

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
    los datos enviados por el formulario.
    '''
    form = BookSearchForm(request.GET or None)

    context = {
        "form": form,
        "submitted_data": None,
        "books": [],
    }

    if form.is_valid():
        cleaned_data = form.cleaned_data
        context["submitted_data"] = form.cleaned_data
        context["books"] = _get_filtered_books(cleaned_data)

    return render(request, "core/search_results.html", context)