from django.core.management.base import BaseCommand

from catalog.services import rebuild_all_embedding_texts

class Command(BaseCommand):
    """
    Regenera el campo embedding_text para todos los libros del catálogo.
    """
    help = "Rebuild embedding_text for all books in the catalog."

    def handle(self, *args, **options):
        """
        Ejecuta la regeneración masiva de embedding_text.
        """
        count = rebuild_all_embedding_texts()

        self.stdout.write(
            self.style.SUCCESS(
                f"embedding_text regenerado correctamente para {count} libro(s)."
            )
        )