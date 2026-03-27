from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):

    context = {
        'name': 'José Antonio'
    }
    return render(
        request,
        'recipes/home.html',
        context=context,
    )

def sobre(request):
    return render(
        request,
        'recipes/sobre.html'
    )

def contato(request):
    return render(
        request,
        'recipes/contato.html'
    )
