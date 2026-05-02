from django import forms

class EmailCaptureForm(forms.Form):
    """
    Formulario simple para capturar email y consentimiento.
    """

    email = forms.EmailField(
        label="Tu correo",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "tuemail@ejemplo.com",
            }
        ),
    )

    consent_newsletter = forms.BooleanField(
        label="Acepto recibir recomendaciones extra y el newsletter del proyecto.",
        required=True,
    )

    search_request_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )