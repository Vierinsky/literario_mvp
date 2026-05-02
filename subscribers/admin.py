from django.contrib import admin

from .models import EmailSubscriber

@admin.register(EmailSubscriber)
class EmailSubscriberAdmin(admin.ModelAdmin):
    """
    Configuración del admin para suscriptores por email.
    """
    list_display = (
        "id",
        "email",
        "source",
        "first_search_request",
        "consent_newsletter",
        "is_active",
        "created_at",
    )
    list_filter = ("source", "consent_newsletter", "is_active", "created_at")
    search_fields = ("email", "provider_contact_id")