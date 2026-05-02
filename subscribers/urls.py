from django.urls import path

from . import views

urlpatterns = [
    path("subscribe/", views.subscribe_email, name="subscribe_email"),
]