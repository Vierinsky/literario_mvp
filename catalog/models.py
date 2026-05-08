from django.db import models

class Author(models.Model):
    '''
    Representa un autor dentro del catálogo.
    '''

    name = models.CharField(max_length=255, db_index=True)
    country = models.CharField(max_length=100, blank=True)
    author_note_short = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        Devuelve una representación legible del autor.
        '''
        return self.name
    
class Book(models.Model):
    '''
    Representa un libro dentro del catálogo del proyecto.

    Este modelo guarda tanto metadata bibliográfica básica como campos
    operativos necesarios para decidir si un libro puede usarse en
    recomendaciones y, más adelante, en procesos de embeddings.
    '''

    class GenreChoices(models.TextChoices):
        '''
        Géneros principales soportados por el MVP.
        '''
        FANTASY = "fantasy", "Fantasía"
        SCIENCE_FICTION = "science_fiction", "Ciencia ficción"

    class LengthCategoryChoices(models.TextChoices):
        '''
        Categorías simples de longitud derivadas desde page_count.
        '''
        SHORT = "short", "Corto"
        MEDIUM = "medium", "Medio"
        LONG = "long", "Largo"

    class CatalogStatusChoices(models.TextChoices):
        '''
        Estado operativo/editorial del libro dentro del catálogo.

        candidate:
            Libro detectado o cargado inicialmente, pero todavía incompleto.

        needs_review:
            Libro con metadata básica suficiente, pero pendiente de revisión humana.

        active:
            Libro aprobado para aparecer en recomendaciones.

        inactive:
            Libro válido, pero temporalmente excluido del recomendador.

        rejected:
            Libro descartado por duplicado, mala metadata o falta de encaje.
        '''
        CANDIDATE = "candidate", "Candidato"
        NEEDS_REVIEW = "needs_review", "Necesita revisión"
        ACTIVE = "active", "Activo"
        INACTIVE = "inactive", "Inactivo"
        REJECTED = "rejected", "Rechazado"

    class MetadataStatusChoices(models.TextChoices):
        '''
        Estado de calidad de la metadata bibliográfica y curatorial.
        '''
        PENDING = "pending", "Pendiente"
        PARTIAL= "partial", "Parcial"
        VALIDATED = "validated", "Validada"
    
    title = models.CharField(max_length=255, db_index=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )
    synopsis = models.TextField()
    genre_main = models.CharField(
        max_length=50,
        choices=GenreChoices.choices,
        db_index=True
    )
    page_count = models.PositiveBigIntegerField(null=True, blank=True)
    length_category = models.CharField(
        max_length=20,
        choices=LengthCategoryChoices.choices,
        blank=True,
        db_index=True,
    )
    available_in_spanish = models.BooleanField(default=True, db_index=True)
    spanish_title = models.CharField(max_length=255, blank=True)
    original_language = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=32, blank=True, db_index=True)
    cover_url = models.URLField(blank=True)
    
    publication_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    # Identificadores externos para poder cruzar y actualizar metadata
    # sin depender solamente de título + autor.
    external_openlibrary_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    external_google_books_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    external_wikidata_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    # Estado operativo/editorial del libro.
    catalog_status = models.CharField(
        max_length=20,
        choices=CatalogStatusChoices.choices,
        default=CatalogStatusChoices.CANDIDATE,
        db_index=True,
    )
    
    # Estado de calidad de metadata.
    metadata_status = models.CharField(
        max_length=20,
        choices=MetadataStatusChoices.choices,
        default=MetadataStatusChoices.PENDING,
        db_index=True,
    )

    # Fecha de última actualización/enriquecimiento desde fuentes externas.
    last_enriched_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    
    embedding_text = models.TextField(blank=True)

    # Interruptor simple para excluir libros del sitio/recomendador.
    # Por ahora se mantiene junto a catalog_status para no romper lógica existente.
    is_active = models.BooleanField(default=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def calculate_length_category(self):
        '''
        Deriva la categoría de longitud a partir de page_count.

        Returns
        -------
        str
            'short', 'medium' o 'long'. Retorna cadena vacía
            si no hay page_count.
        '''
        if not self.page_count:
            return ""
        
        if self.page_count < 300:
            return self.LengthCategoryChoices.SHORT
        
        if self.page_count <= 600:
            return self.LengthCategoryChoices.MEDIUM
        
        return self.LengthCategoryChoices.LONG
    
    
    def is_ready_for_recommendations(self):
        '''
        Indica si el libro cumple condiciones mínimas para ser recomendado.

        Esta validación no reemplaza validaciones más completas del catálogo,
        pero sirve como regla rápida dentro del modelo.

        Returns
        -------
        bool
            True si el libro puede participar en recomendaciones.
            False en caso contrario.
        '''
        has_basic_metadata = all([
            self.title,
            self.author_id,
            self.synopsis,
            self.genre_main,
            self.length_category,
        ])


    def save(self, *args, **kwargs):
        '''
        Recalcula la categoría de longitud antes de guardar.
        '''
        self.length_category = self.calculate_length_category()
        super().save(*args, **kwargs)

    def __str__(self):
        '''
        Devuelve una representación legible del libro.
        '''
        return f"{self.title} - {self.author.name}"
    
class BookTag(models.Model):
    '''
    Representa un tag curatorial asociado a un libro.
    '''

    class TagTypeChoices(models.TextChoices):
        TONE_PRIMARY = "tone_primary", "Tono principal"
        TONE_SECONDARY = "tone_secondary", "Tono secundario"
        PACE = "pace", "Ritmo"
        THEME = "theme", "Temática"

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="tags",
    )
    tag_type = models.CharField(
        max_length=50,
        choices=TagTypeChoices.choices,
        db_index=True,
    )
    tag_value = models.CharField(
        max_length=100,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book", "tag_type", "tag_value"],
                name="unique_book_tag_type_value",
            )
        ]

    def __str__(self):
        """
        Devuelve una representación legible del tag.
        """
        return f"{self.book.title} | {self.tag_type}: | {self.tag_value}"
        
