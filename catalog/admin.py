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

    El objetivo de esta vista es facilitar la revisión operativa del
    catálogo: estado del libro, calidad de metadata, disponibilidad,
    fuentes externas y preparación futura para embeddings.
    '''

    list_display = (
        "id",
        "title",
        "author",
        "genre_main",
        "catalog_status",
        "metadata_status",
        "length_category",
        "available_in_spanish",
        "is_active",
        "updated_at",
    )
    list_filter = (
        "genre_main",
        "catalog_status",
        "metadata_status",
        "length_category",
        "available_in_spanish",
        "is_active"
        )
    search_fields = (
        "title", 
        "author__name", 
        "isbn",
        "external_openlibrary_id",
        "external_google_books_id",
        "external_wikidata_id",
        )
    readonly_fields = (
        "created_at",
        "updated_at",
        "last_enriched_at",
    )
    fieldsets = (
        (
            "Información básica",
            {
                "fields": (
                    "title",
                    "author",
                    "synopsis",
                    "genre_main",
                    "page_count",
                    "length_category",
                )
            },
        ),
        (
            "Disponibilidad e idioma",
            {
                "fields": (
                    "available_in_spanish",
                    "spanish_title",
                    "original_language",
                )
            },
        ),
        (
            "Metadata bibliográfica",
            {
                "fields": (
                    "isbn",
                    "publication_year",
                    "cover_url",
                )
            },
        ),
        (
            "Estado operativo del catálogo",
            {
                "fields": (
                    "catalog_status",
                    "metadata_status",
                    "is_active",
                )
            },
        ),
        (
            "Identificadores externos",
            {
                "fields": (
                    "external_openlibrary_id",
                    "external_google_books_id",
                    "external_wikidata_id",
                    "last_enriched_at",
                )
            },
        ),
        (
            "Preparación semántica",
            {
                "fields": (
                    "embedding_text",
                )
            },
        ),
        (
            "Fechas internas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    actions = (
        "mark_as_active_partial",
        "mark_as_needs_review",
        "mark_as_inactive",
    )

    @admin.action(description="Marcar como activo con metadata parcial")
    def mark_as_active_partial(self, request, queryset):
        '''
        Marca libros seleccionados como activos y con metadata parcial.

        Esta acción es útil para aprobar libros que ya están suficientemente
        curados para participar en recomendaciones, aunque todavía no tengan
        validación completa.
        '''
        updated_count = queryset.update(
            catalog_status=Book.CatalogStatusChoices.ACTIVE,
            metadata_status=Book.MetadataStatusChoices.PARTIAL,
            is_active=True,
        )

        self.message_user(
            request,
            f"{updated_count} libro(s) marcado(s) como activos con metadata parcial.",
        )

    @admin.action(description="Marcar como necesita revisión")
    def mark_as_needs_review(self, request, queryset):
        '''
        Marca libros seleccionados como pendientes de revisión humana.
        '''
        updated_count = queryset.update(
            catalog_status=Book.CatalogStatusChoices.NEEDS_REVIEW,
            metadata_status=Book.MetadataStatusChoices.PARTIAL,
        )

        self.message_user(
            request,
            f"{updated_count} libro(s) marcado(s) como necesita revisión.",
        )

    @admin.action(description="Marcar como inactivo")
    def mark_as_inactive(self, request, queryset):
        '''
        Desactiva libros seleccionados para que no participen en recomendaciones.
        '''
        updated_count = queryset.update(
            catalog_status=Book.CatalogStatusChoices.INACTIVE,
            is_active=False,
        )

        self.message_user(
            request,
            f"{updated_count} libro(s) marcado(s) como inactivos.",
        )

@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    '''
    Configuración del admin para tags curatoriales.
    '''

    list_display = ("id", "book", "tag_type", "tag_value", "created_at")
    list_filter = ("tag_type",)
    search_fields = ("book__title", "tag_value")
