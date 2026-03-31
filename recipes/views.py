from django.http import HttpResponse
from django.shortcuts import render
from utils.recipes.factoty import make_recipe
from recipes.models import Recipe


# Create your views here.


def index(request):
    recipes = Recipe.objects.all().order_by('-id')
    context = {
        'name': 'José Antonio',
        'recipes': recipes,
    }
    return render(
        request,
        'recipes/pages/home.html',
        context=context,
    )

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id).order_by('-id')
    context = {
        'name': 'José Antonio',
        'recipes': recipes,
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
        'is_detail_page':True,
    }
    return render(
        request,
        'recipes/pages/recipe-view.html',
        context=context,

    )
