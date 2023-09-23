from django.urls import path
from web import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tag/<slug:slug>/", views.tag, name="tagged"),
]
