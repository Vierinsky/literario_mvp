from django.db import models
from django.utils import timezone

class EditorialPost(models.Model):
    """
    Representa una pieza editorial del proyecto.
    """

    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, max_length=255)
    summary = models.TextField(blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Si se publica y no tiene fecha de publicación, la asigna.
        """
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Devuelve una representación legible del post.
        """
        return self.title

class EditorialPostBook(models.Model):
    """
    Relaciona un post editorial con libros del catálogo.
    """

    editorial_post = models.ForeignKey(
        EditorialPost,
        on_delete=models.CASCADE,
        related_name="post_books",
    )
    book = models.ForeignKey(
        "catalog.Book",
        on_delete=models.CASCADE,
        related_name="editorial_links",
    )
    position = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["editorial_post", "book"],
                name="unique_editorial_post_book",
            ),
            models.UniqueConstraint(
                fields=["editorial_post", "position"],
                name="unique_editorial_post_position",
            ),
        ]
        ordering = ["position"]

    def __str__(self):
        """
        Devuelve una representación legible del vínculo.
        """
        return f"{self.editorial_post.title} | #{self.position} | {self.book.title}"
    