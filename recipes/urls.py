from django.urls import path, include
from django.http import HttpResponse
from . import views

app_name = 'recipes'

urlpatterns = [
    path("", views.index, name="home"),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
]
