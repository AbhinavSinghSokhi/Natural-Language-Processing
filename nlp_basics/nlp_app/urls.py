from django.urls import path, include
from . import views

urlpatterns=[
    path("", views.index, name="indexPage"),
    path("promptProcessing", views.prompt_processing, name="prompt_processing"),
    # path("reponse", views.)
]