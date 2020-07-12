from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("wikiPLUS/new/", views.post_new, name="post_new"),
    path('wikiPLUS/edit/<str:name>', views.post_edit, name='post_edit'),
    path("search", views.search, name="search"),
    path("wiki/<str:name>", views.pages, name="pages"),
    
]
