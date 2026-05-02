from django.shortcuts import redirect, render
from django.utils import timezone

from tracking.models import SearchRequest

from .forms import EmailCaptureForm
from .models import EmailSubscriber

def subscribe_email(request):
    """
    Captura un email desde la página de resultados.
    """
    if request.method != "POST":
        return redirect("home")
    
    form = EmailCaptureForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "subscribers/subscription_result.html",
            {
                "success": False,
                "message": "No pude procesar el formulario. Revisa el correo y el consentimiento",
            },
        )
    
    email = form.cleaned_data["email"]
    consent_newsletter = form.cleaned_data["consent_newsletter"]
    search_request_id = form.cleaned_data.get("search_request_id")

    first_search_request = None
    if search_request_id:
        first_search_request = SearchRequest.objects.filter(id=search_request_id).first()

    subscriber, created = EmailSubscriber.objects.update_or_create(
        email=email,
        defaults={
            "source": EmailSubscriber.SourceChoices.SEARCH_RESULTS,
            "consent_newsletter": consent_newsletter,
            "consent_timestamp": timezone.now() if consent_newsletter else None,
            "first_search_request": first_search_request,
            "is_active": True,
        },
    )

    if created:
        message = "Tu correo fue registrado correctamente."
    else:
        message = "Tu correo ya existía y actualicé su información."

    return render(
        request,
        "subscribers/subscription_result.html",
        {
            "success": True,
            "message": message,
            "subscriber": subscriber,
            "first_search_request": first_search_request,
        },
    )

