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
        FANTASY = "fantasy", "Fantasía"
        SCIENCE_FICTION = "science_fiction", "Ciencia ficción"

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