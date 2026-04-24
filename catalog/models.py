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
    '''

    class GenreChoices(models.TextChoices):
        FANTASY = "fantasy", "Fantasia"
        SCIENCE_FICTION = "science_fiction", "Ciencia ficcion"

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
    available_in_spanish = models.BooleanField(default=True, db_index=True)
    spanish_title = models.CharField(max_length=255, blank=True)
    original_language = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=32, blank=True, db_index=True)
    cover_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upgraded_at = models.DateTimeField(auto_now=True)

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
        THEME = "theme", "Tematica"

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
                name= "unique_book_tag_type_value",
            )
        ]

    def __str__(self):
        """
        Devuelve una representación legible del tag.
        """
        return f"{self.book.title} | {self.tag_type}: | {self.tag_value}"
        