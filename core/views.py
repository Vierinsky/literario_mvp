from django.shortcuts import render

from recommendations.services import get_filtered_books
from subscribers.forms import EmailCaptureForm
from tracking.services import persist_search

from .forms import BookSearchForm


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
        search_request = persist_search(request, cleaned_data, results)

        context["submitted_data"] = cleaned_data
        context["results"] = results
        context["email_form"] = EmailCaptureForm(
            initial={"search_request_id": search_request.id}
        )

    return render(request, "core/search_results.html", context)
