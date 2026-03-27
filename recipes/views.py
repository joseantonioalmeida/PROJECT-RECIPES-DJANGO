from django.http import HttpResponse
from django.shortcuts import render
from utils.recipes.factoty import make_recipe

# Create your views here.


def index(request):

    context = {
        'name': 'José Antonio',
        'recipes': [make_recipe() for _ in range(10)],
    }
    return render(
        request,
        'recipes/pages/home.html',
        context=context,
    )


def recipe(request, id):

    context = {
        'name': 'José Antonio',
        'recipe': make_recipe(),
    }
    return render(
        request,
        'recipes/pages/recipe-view.html',
        context=context,
    )
