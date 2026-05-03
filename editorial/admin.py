from django.contrib import admin

from .models import EditorialPost, EditorialPostBook

@admin.register(EditorialPost)
class EditorialPostAdmin(admin.ModelAdmin):
    """
    Configuración del admin para piezas editoriales.
    """

    list_display = (
        "id",
        "title",
        "is_published",
        "published_at",
        "created_at",
    )
    list_filter = ("is_published", "published_at", "created_at")
    search_fields = ("title", "slug", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(EditorialPostBook)
class EditorialPostBookAdmin(admin.ModelAdmin):
    """
    Configuración del admin para relaciones entre posts y libros.
    """

    list_display = ("id", "editorial_post", "book", "position")
    list_filter = ("editorial_post",)
    search_fields = ("editorial_post__title", "book__title")