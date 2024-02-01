from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("wiki/random/", views.random_page, name="random"),
    path("create/", views.create_page, name="create"),
    path("wiki/edit/<str:name>", views.edit_page, name="edit") 
]
