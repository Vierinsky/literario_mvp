from django.shortcuts import render

# from .models import Book


# def book_list(request):
#     '''
#     Renderiza una lista pública simple de libros activos del catálogo.
#     '''
#     books = (
#         Book.objects.filter(is_active=True)
#         .select_related("author")
#         .order_by("title")
#     )

#     context = {
#         "books": books,
#     }

#     return render(request, "catalog/book_list.html", context)