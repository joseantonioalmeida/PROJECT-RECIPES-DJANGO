from django.urls import path, include
from django.http import HttpResponse
from . import views

app_name = 'recipes'

urlpatterns = [
    path("", views.RecipeListViewBase.as_view(), name="home"),
    path('recipes/search/', views.search , name="search"),#type:ignore
    path('recipes/category/<int:category_id>/', views.category, name="category"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
]
