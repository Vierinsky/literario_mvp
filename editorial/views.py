from django.shortcuts import get_object_or_404, render

from .models import EditorialPost

def editorial_index(request):
    """
    Renderiza el índice público de piezas editoriales publicadas.
    """
    posts = (
        EditorialPost.objects.filter(is_published=True)
        .order_by("-published_at", "-created_at")
    )

    context = {
        "posts": posts,
    }

    return render(request, "editorial/index.html", context)


def editorial_detail(request, slug):
    """
    Renderiza el detalle de una pieza editorial publicada.
    """
    post = get_object_or_404(
        EditorialPost.objects.prefetch_related("post_books__book"),
        slug=slug,
        is_published=True,
    )

    context = {
        "post": post,
    }

    return render(request, "editorial/detail.html", context)
