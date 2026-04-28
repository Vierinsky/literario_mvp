from django.contrib import admin

from .models import Author, Book, BookTag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    '''
    Configuración del admin para autores.
    '''
    
    list_display = ("id", "name", "country", "created_at")
    search_fields = ("name", "country")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    '''
    Configuración del admin para libros.
    '''

    list_display = (
        "id",
        "title",
        "author",
        "genre_main",
        "length_category",
        "available_in_spanish",
        "is_active",
    )
    list_filter = ("genre_main", "length_category", "available_in_spanish", "is_active")
    search_fields = ("title", "author__name", "isbn")

@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    '''
    Configuración del admin para tags curatoriales.
    '''

    list_display = ("id", "book", "tag_type", "tag_value", "created_at")
    list_filter = ("tag_type",)
    search_fields = ("book__title", "tag_value")
