from django.shortcuts import render



def home(request):
    '''
    Renderiza la página de inicio del proyecto.
    '''
    return render(request, "core/home.html")


def about(request):
    '''
    Renderiza la página sobre el proyecto.
    '''
    return render(request, "core/about.html")