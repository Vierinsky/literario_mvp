from django.shortcuts import render

from .models import Book

def home(request):
    '''
    Renderiza la página de inicio del proyecto.
    '''
    return render(request, "core/home.html")


def about(request):
    '''
    Renderiza la página sobre el proyecto.
    '''
    return render(request, "core/about.html")


def book_list(request):
    '''
    Renderiza una lista pública simple de libros activos del catálogo.
    '''
    books = (
        Book.objects.filter(is_active=True)
        .select_related("author")
        .order_by("title")
    )

    context = {
        "books": books,
    }

    return render(request, "catalog/book_list.html", context)