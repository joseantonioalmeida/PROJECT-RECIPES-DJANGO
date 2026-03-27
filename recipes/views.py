from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):

    context = {
        'name': 'José Antonio'
    }
    return render(
        request,
        'recipes/pages/home.html',
        context=context,
    )


def recipe(request, id):

    context = {
        'name': 'José Antonio'
    }
    return render(
        request,
        'recipes/pages/recipe-view.html',
        context=context,
    )
