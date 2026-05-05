from catalog.models import Author, Book, BookTag


books_seed = [
    {
        "author_name": "Patrick Rothfuss",
        "country": "United States",
        "author_note_short": "Autor de fantasía contemporánea conocido por una voz lírica y melancólica.",
        "title": "El nombre del viento",
        "synopsis": "Novela de fantasía sobre memoria, identidad, música, magia y formación, con un tono melancólico y una narración más íntima que épica.",
        "genre_main": Book.GenreChoices.FANTASY,
        "page_count": 660,
        "available_in_spanish": True,
        "spanish_title": "El nombre del viento",
        "original_language": "English",
        "tags": [
            ("tone_primary", "melancholic"),
            ("tone_secondary", "strange"),
            ("pace", "contemplative"),
            ("theme", "mythic_reimagining"),
        ],
    },
    {
        "author_name": "Brandon Sanderson",
        "country": "United States",
        "author_note_short": "Autor de fantasía conocido por sistemas de magia robustos y narrativa accesible.",
        "title": "Nacidos de la bruma: El imperio final",
        "synopsis": "Fantasía con intriga política, magia estructurada, rebelión y ritmo ágil, en un mundo oscuro donde todavía queda espacio para la esperanza.",
        "genre_main": Book.GenreChoices.FANTASY,
        "page_count": 540,
        "available_in_spanish": True,
        "spanish_title": "Nacidos de la bruma: El imperio final",
        "original_language": "English",
        "tags": [
            ("tone_primary", "dark"),
            ("tone_secondary", "hopeful"),
            ("pace", "fast"),
            ("theme", "political_intrigue"),
        ],
    },
    {
        "author_name": "Joe Abercrombie",
        "country": "United Kingdom",
        "author_note_short": "Autor asociado a la fantasía grimdark contemporánea.",
        "title": "La voz de las espadas",
        "synopsis": "Dark fantasy centrada en violencia, cinismo, personajes rotos e intriga, con un tono oscuro y una mirada áspera del heroísmo.",
        "genre_main": Book.GenreChoices.FANTASY,
        "page_count": 530,
        "available_in_spanish": True,
        "spanish_title": "La voz de las espadas",
        "original_language": "English",
        "tags": [
            ("tone_primary", "dark"),
            ("tone_secondary", "unsettling"),
            ("pace", "balanced"),
            ("theme", "grimdark"),
        ],
    },
    {
        "author_name": "Ursula K. Le Guin",
        "country": "United States",
        "author_note_short": "Autora clave de fantasía y ciencia ficción con sensibilidad filosófica y atmosférica.",
        "title": "La mano izquierda de la oscuridad",
        "synopsis": "Ciencia ficción contemplativa sobre política, cultura, identidad y extrañeza, con una atmósfera melancólica y un enfoque más reflexivo que espectacular.",
        "genre_main": Book.GenreChoices.SCIENCE_FICTION,
        "page_count": 300,
        "available_in_spanish": True,
        "spanish_title": "La mano izquierda de la oscuridad",
        "original_language": "English",
        "tags": [
            ("tone_primary", "melancholic"),
            ("tone_secondary", "strange"),
            ("pace", "contemplative"),
            ("theme", "political_intrigue"),
        ],
    },
    {
        "author_name": "Jeff VanderMeer",
        "country": "United States",
        "author_note_short": "Autor asociado a la weird fiction y la ciencia ficción inquietante.",
        "title": "Aniquilación",
        "synopsis": "Novela breve e inquietante sobre exploración, transformación y extrañeza biológica, con una atmósfera densa, rara y perturbadora.",
        "genre_main": Book.GenreChoices.SCIENCE_FICTION,
        "page_count": 200,
        "available_in_spanish": True,
        "spanish_title": "Aniquilación",
        "original_language": "English",
        "tags": [
            ("tone_primary", "unsettling"),
            ("tone_secondary", "strange"),
            ("pace", "contemplative"),
            ("theme", "horror"),
        ],
    },
]


for item in books_seed:
    author, _ = Author.objects.get_or_create(
        name=item["author_name"],
        defaults={
            "country": item["country"],
            "author_note_short": item["author_note_short"],
        },
    )

    book, _ = Book.objects.update_or_create(
        title=item["title"],
        author=author,
        defaults={
            "synopsis": item["synopsis"],
            "genre_main": item["genre_main"],
            "page_count": item["page_count"],
            "available_in_spanish": item["available_in_spanish"],
            "spanish_title": item["spanish_title"],
            "original_language": item["original_language"],
            "isbn": "",
            "cover_url": "",
            "is_active": True,
        },
    )

    BookTag.objects.filter(book=book).delete()

    for tag_type, tag_value in item["tags"]:
        BookTag.objects.create(
            book=book,
            tag_type=tag_type,
            tag_value=tag_value,
        )

    print(f"Cargado: {book.title} | length_category={book.length_category}")