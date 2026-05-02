from django.urls import path

from . import views

urlpatterns = [
    path("", views.editorial_index, name="editorial_index"),
    path("<slug:slug>/", views.editorial_detail, name="editorial_detail"),
]