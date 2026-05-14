import json
from pathlib import Path
import requests

from django.core.management.base import BaseCommand

from catalog.external_sources import get_openlibrary_candidates


def save_candidates_to_json(candidates, output_path, query_metadata):
    """
    Guarda candidatos normalizados en un archivo JSON.

    Parameters
    ----------
    candidates : list[dict]
        Lista de candidatos normalizados desde fuentes externas.

    output_path : str
        Ruta donde se guardará el archivo JSON.

    query_metadata : dict
        Metadata de la consulta realizada, como título, autor y fuente.

    Returns
    -------
    Path
        Ruta final del archivo guardado.
    """
    path = Path(output_path)

    # Crea la carpeta destino si todavía no existe
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "query": query_metadata,
        "candidates": candidates,
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            payload,
            file,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

    return path

class Command(BaseCommand):
    """
    Busca metadata de un libro en fuentes externas.

    En esta primera versión solo consulta Open Library. Más adelante
    se podrán agregar Google Books y Wikidata sin cambiar la interfaz
    principal del comando.
    """
    help = "Busca metadata externa para un libro por título y autor."

    def add_arguments(self, parser):
        """
        Define argumentos del comando.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser usado por Django para argumentos de management commands.
        """
        parser.add_argument(
            "--title",
            required=True,
            help="Título del libro a buscar.",
        )

        parser.add_argument(
            "--author",
            required=False,
            default="",
            help="Autor del libro a buscar.",
        )

        parser.add_argument(
            "--limit",
            required=False,
            type=int,
            default=5,
            help="Cantidad máxima de resultados a mostrar.",
        )

        parser.add_argument(
            "--output",
            required=False,
            default="",
            help="Ruta opcional para guardar los candidatos normalizados en JSON.",
        )

    def handle(self, *args, **options):
        """
        Ejecuta la búsqueda de metadata externa.

        Parameters
        ----------
        *args : tuple
            Argumentos posicionales no usados.

        **options : dict
            Opciones del comando.
        """
        title = options["title"]
        author = options["author"]
        limit = options["limit"]
        output = options["output"]

        self.stdout.write("")
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f"Buscando metadata para: {title}"
            )
        )

        if author:
            self.stdout.write(f"Autor esperado: {author}")

        self.stdout.write("Fuente: Open Library")
        self.stdout.write("")

        try:
            candidates = get_openlibrary_candidates(
                title=title,
                author=author,
                limit=limit,
            )
        except requests.exceptions.Timeout:
            self.stdout.write(
                self.style.ERROR(
                    "La consulta a Open Library agotó el tiempo de espera."
                )
            )
            return
        except requests.exceptions.RequestException as error:
            self.stdout.write(
                self.style.ERROR(
                    f"Error consultando Open Library: {error}"
                )
            )
            return

        if not candidates:
            self.stdout.write(
                self.style.WARNING("No se encontraron candidatos.")
            )
            return

        for index, candidate in enumerate(candidates, start=1):
            self.stdout.write(f"[{index}] {candidate['title']}")
            self.stdout.write(
                f"    Match score: {candidate.get('match_score', 0)}"
            )
            self.stdout.write(f"    Autor: {candidate['author_name']}")
            self.stdout.write(
                f"    Año: {candidate['publication_year'] or 'sin dato'}"
            )
            self.stdout.write(f"    ISBN: {candidate['isbn'] or 'sin dato'}")
            self.stdout.write(
                f"    Open Library ID: {candidate['external_openlibrary_id']}"
            )
            
            language_hints = candidate.get("language_hints", [])
            
            self.stdout.write(
                f"    Idiomas detectados: {', '.join(language_hints) if language_hints else 'sin dato'}"
            )
            self.stdout.write(
                f"    Cover: {candidate['cover_url'] or 'sin dato'}"
            )


            subjects = candidate.get("subjects", [])

            if subjects:
                self.stdout.write(
                    f"    Subjects: {', '.join(subjects[:8])}"
                )

            self.stdout.write("")

        if output:
            saved_path = save_candidates_to_json(
                candidates=candidates,
                output_path=output,
                query_metadata={
                    "title": title,
                    "author": author,
                    "source": "openlibrary",
                    "limit": limit,
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Candidatos guardados en: {saved_path}"
                )
            )

