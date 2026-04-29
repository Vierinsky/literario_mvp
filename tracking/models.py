from django.db import models

class SearchRequest(models.Model):
    '''
    Representa una búsqueda realizada por un visitante anónimo.
    En esta etapa no la vinculamos todavía a EmailSubscriber.
    '''

    session_id = models.CharField(max_length=64, db_index=True)
    query_text = models.TextField(blank=True)
    tone_filter = models.CharField(max_length=50, blank=True, db_index=True)
    pace_filter = models.CharField(max_length=50, blank=True, db_index=True)
    theme_filter = models.CharField(max_length=100, blank=True, db_index=True)
    length_filter = models.CharField(max_length=20, blank=True, db_index=True)
    include_english = models.BooleanField(default=False, db_index=True)
    user_agent_hash = models.CharField(max_length=128, blank=True)
    ip_hash = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        """
        Devuelve una representación breve de la búsqueda.
        """
        query_preview = self.query_text[:40] if self.query_text else "sin texto"
        return f"{self.session_id} | {query_preview}"
    
class SearchResult(models.Model):
    """
    Representa un resultado mostrado al usuario para una búsqueda.
    """

    search_request = models.ForeignKey(
        SearchRequest,
        on_delete=models.CASCADE,
        related_name="results",
    )
    book = models.ForeignKey(
        "catalog.Book",
        on_delete=models.CASCADE,
        related_name="search_results",
    )
    rank_position = models.PositiveSmallIntegerField(db_index=True)
    match_explanation = models.TextField()
    shown_to_user = models.BooleanField(default=True)
    clicked = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        contraints = [
            models.UniqueConstraint(
                fields=["search_request", "rank_position"],
                name="unique_search_request_rank_position",
            ),
            models.UniqueConstraint(
                fields=["search_request", "book"],
                name="unique_search_request_book",
            ),
        ]

        def __str__(self):
            """
            Devuelve una representación breve del resultado.
            """
            return f"SearchRequest {self.search_request_id} | #{self.rank_position} | {self.book.title}"
