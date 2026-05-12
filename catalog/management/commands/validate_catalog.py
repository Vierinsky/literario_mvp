from django.core.management.base import BaseCommand

from catalog.models import Book
from catalog.services import (
    get_catalog_quality_issues,
    is_book_ready_for_embedding_text,
    is_book_ready_for_recommendation,
)


class Command(BaseCommand):
    """
    Valida la calidad mínima del catálogo literario.

    Este comando revisa los libros existentes y reporta:
    - estado operativo;
    - estado de metadata;
    - si están listos para recomendación;
    - si están listos para construir embedding_text;
    - problemas de calidad detectados.
    """

    help = "Valida la calidad mínima del catálogo de libros."

    def add_arguments(self, parser):
        """
        Define argumentos opcionales para el comando.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser usado por Django para argumentos de management commands.
        """
        parser.add_argument(
            "--only-problems",
            action="store_true",
            help="Muestra solo libros con problemas de calidad.",
        )

        parser.add_argument(
            "--only-active",
            action="store_true",
            help="Revisa solo libros con catalog_status='active'.",
        )

    def handle(self, *args, **options):
        """
        Ejecuta la validación del catálogo.

        Parameters
        ----------
        *args : tuple
            Argumentos posicionales no usados.

        **options : dict
            Opciones entregadas desde la línea de comandos.
        """
        only_problems = options["only_problems"]
        only_active = options["only_active"]

        books = (
            Book.objects
            .select_related("author")
            .prefetch_related("tags")
            .order_by("title")
        )

        if only_active:
            books = books.filter(
                catalog_status=Book.CatalogStatusChoices.ACTIVE
            )

        total_books = 0
        books_with_issues = 0
        ready_for_recommendation = 0
        ready_for_embedding_text = 0

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Validación del catálogo"))
        self.stdout.write("")

        for book in books:
            total_books += 1

            issues = get_catalog_quality_issues(book)
            ready_recommendation = is_book_ready_for_recommendation(book)
            ready_embedding_text = is_book_ready_for_embedding_text(book)

            if issues:
                books_with_issues += 1

            if ready_recommendation:
                ready_for_recommendation += 1

            if ready_embedding_text:
                ready_for_embedding_text += 1

            if only_problems and not issues:
                continue

            self.stdout.write(f"- {book.title} — {book.author.name}")
            self.stdout.write(f"  catalog_status: {book.catalog_status}")
            self.stdout.write(f"  metadata_status: {book.metadata_status}")
            self.stdout.write(f"  is_active: {book.is_active}")
            self.stdout.write(f"  listo recomendación: {ready_recommendation}")
            self.stdout.write(f"  listo embedding_text: {ready_embedding_text}")

            if issues:
                self.stdout.write(self.style.WARNING("  Problemas:"))

                for issue in issues:
                    self.stdout.write(f"    - {issue}")
            else:
                self.stdout.write(self.style.SUCCESS("  Sin problemas mínimos."))

            self.stdout.write("")

        self.stdout.write(self.style.MIGRATE_HEADING("Resumen"))
        self.stdout.write(f"Libros revisados: {total_books}")
        self.stdout.write(f"Libros con problemas: {books_with_issues}")
        self.stdout.write(
            f"Listos para recomendación: {ready_for_recommendation}"
        )
        self.stdout.write(
            f"Listos para embedding_text: {ready_for_embedding_text}"
        )
        self.stdout.write("")

        if books_with_issues:
            self.stdout.write(
                self.style.WARNING(
                    "Validación finalizada con problemas detectados."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Validación finalizada sin problemas mínimos."
                )
            )