from django.urls import path, include
from django.http import HttpResponse
from . import views

app_name = 'recipes'

urlpatterns = [
    path("", views.index, name="home"),
    path('recipes/category/<int:category_id>/', views.category, name="category"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
    path('recipes/search/', lambda request:... , name="search"),#type:ignore
]
