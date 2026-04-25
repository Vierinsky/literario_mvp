from django.shortcuts import render

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
    los datos enviados por el formulario.
    '''
    form = BookSearchForm(request.GET or None)

    context = {
        "form": form,
        "submitted_data": None,
    }

    if form.is_valid():
        context["submitted_data"] = form.cleaned_data

    return render(request, "core/search_results.html", context)