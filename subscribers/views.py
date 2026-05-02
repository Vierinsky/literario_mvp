from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import EmailCaptureForm
from .models import EmailSubscriber

def subscribe_email(request):
    """
    Captura un email desde la página de resultados.
    """
    if request.method != "POST":
        return redirect("home")
    
    form = EmailCaptureForm(request.PoST)

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

    subscriber, created = EmailSubscriber.objects.update_or_create(
        email=email,
        defaults={
            "source": EmailSubscriber.SourceChoices.SEARCH_RESULTS,
            "consent_newsletter": consent_newsletter,
            "consent_timestamp": timezone.now() if consent_newsletter else None,
            "is_active": True,
        },
    )

    if created:
        message = "Tu correo fue registrado correctamente."
    else:
        message = "Tu correo ya existía y actualicé su información."

    return render(
        request,
        "subscriber/subscription_result.html",
        {
            "success": True,
            "message": message,
            "subscriber": subscriber,
        },
    )

