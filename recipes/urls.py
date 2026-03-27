from django.urls import path, include
from django.http import HttpResponse
from . import views

app_name = 'recipes'

urlpatterns = [
    path("", views.index, name="home"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
]
