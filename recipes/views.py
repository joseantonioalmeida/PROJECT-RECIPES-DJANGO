from django.http import Http404
from django.shortcuts import render, redirect
from utils.recipes.factoty import make_recipe
from recipes.models import Recipe


# Create your views here.


def index(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {
        'recipes': recipes,
    }
    return render(
        request,
        'recipes/pages/home.html',
        context=context,
    )

def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
        ).order_by('-id')
    
    if not recipes:
        raise Http404('Not Found')

    context = {
        'recipes': recipes,
        'title': f'{recipes.first().category.name} - Category |' #type:ignore
    }
    return render(
        request,
        'recipes/pages/category.html',
        context=context,
    )


def recipe(request, id):

    context = {
        'recipe': make_recipe(),
        'is_detail_page':True,
    }
    return render(
        request,
        'recipes/pages/recipe-view.html',
        context=context,

    )
