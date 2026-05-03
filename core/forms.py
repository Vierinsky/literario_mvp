from django import forms


class BookSearchForm(forms.Form):
    '''
    Formulario inicial del recomendador literario.
    Captura texto libre y filtros básicos del MVP.
    '''
# OJO con la seguridad; No confiar en nada de lo que ingrese el usuario

    query_text = forms.CharField(
        label="Qué te gustaría leer?",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Ej: magia, melancolía, atmósfera extraña, fantasía íntima...",
            }
        ),
    )

    tone = forms.ChoiceField(
        label="Tono",
        required=False,
        choices=[
            ("", "---------"),
            ("hopeful", "Esperanzador"),
            ("melancholic", "Melancólico"),
            ("dark", "Oscuro"),
            ("unsettling", "Inquietante"),
            ("strange", "Extraño"),
        ],
    )

    pace = forms.ChoiceField(
        label="Ritmo",
        required=False,
        choices=[
            ("", "---------"),
            ("contemplative", "Lento / contemplativo"),
            ("balanced", "Equilibrado"),
            ("fast", "Ágil / rápido"),
        ],
    )

    length = forms.ChoiceField(
        label="Longitud",
        required=False,
        choices=[
            ("", "---------"),
            ("short", "Corto"),
            ("medium", "Medio"),
            ("long", "Largo"),
        ],
    )

    theme = forms.ChoiceField(
        label="Temática",
        required=False,
        choices=[
            ("", "---------"),
            ("romantasy", "Romantasy"),
            ("cozy", "Cozy fantasy / cozy sci-fi"),
            ("dystopia", "Distopía"),
            ("horror", "Horror"),
            ("space_opera", "Space opera"),
            ("grimdark", "Grimdark / dark fantasy"),
            ("cli_fi", "Cli-fi / ficción climática"),
            ("political_intrigue", "Intriga política"),
            ("mythic_reimagining", "Mitología / reimaginación"),
            ("first_contact", "Primer contacto alienígena"), # ¿Borrar la palabra alienígena y cambiarla por un emoji?
        ],
    )

    include_english = forms.BooleanField(
        label="Incluir también libros solo en inglés",
        required=False,
    )

