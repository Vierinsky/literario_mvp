from django.contrib import admin

from .models import SearchRequest, SearchResult

@admin.register(SearchRequest)
class SearchRequestAdmin(admin.ModelAdmin):
    """
    Configuración del admin para búsquedas realizadas.
    """

    list_display = (
        "id",
        "session_id",
        "query_text",
        "tone_filter",
        "pace_filter",
        "theme_filter",
        "length_filter",
        "include_english",
        "created_at",
    )
    list_filter = (
        "tone_filter",
        "pace_filter",
        "theme_filter",
        "length_filter",
        "include_english",
        "created_at",
    )
    search_fields = ("session_id", "query_text")


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    """
    Configuración del admin para resultados mostrados.
    """

    list_display = (
        "id",
        "search_request",
        "book",
        "rank_position",
        "shown_to_user",
        "clicked",
        "created_at",
    )
    list_filter = ("shown_to_user", "clicked", "created_at")
    search_fields = ("book__title", "search_request__query_text", "search_request__session_id")