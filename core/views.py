from django.http import HttpResponse



def home(request):
    '''
    Vista temporal de la página de inicio.
    '''
    return HttpResponse("Home del proyecto literario")


def about(request):
    '''
    Vista temporal de la página sobre el proyecto.
    '''
    return HttpResponse("sobre el proyecto literario")