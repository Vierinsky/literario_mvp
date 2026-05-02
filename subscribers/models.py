from django.db import models

class EmailSubscriber(models.Model):
    '''
    Representa a una persona que dejó su email y consintió
    recibir comunicaciones del proyecto.
    '''
    class SourceChoices(models.TextChoices):
        SEARCH_RESULTS = "search_results", "Resultados de búsqueda"
        NEWSLETTER_PAGE = "newsletter_page", "Página de newsletter"
        EDITORIAL_PAGE = "editorial_page", "Página editorial"
        OTHER = "other", "Otro"

    email = models.EmailField(unique=True, db_index=True)
    source = models.CharField(
        max_length=50,
        choices=SourceChoices.choices,
        db_index=True,
    )
    consent_newsletter = models.BooleanField(default=False)
    consent_timestamp = models.DateField(null=True, blank=True)
    first_search_request = models.ForeignKey(
        "tracking.SearchRequest",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="first_subscriber_links",
    )
    provider_contact_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Devuelve una representación legible del suscriptor.
        """
        return self.email