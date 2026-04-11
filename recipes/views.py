from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range

# Create your views here.


def index(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(recipes, 9)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )
    context = {
        'recipes': page_obj,
        'pagination_range':pagination_range
    }
    return render(
        request,
        'recipes/pages/home.html',
        context=context,
    )

def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    context = {
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category |' #type:ignore
    }
    return render(
        request,
        'recipes/pages/category.html',
        context=context,
    )


def recipe(request, id):
    recipe = get_object_or_404(
        Recipe,
        is_published=True,
        pk=id,
    )

    context = {
        'recipe': recipe,
        'is_detail_page':True,
    }
    return render(
        request,
        'recipes/pages/recipe-view.html',
        context=context,

    )

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True,
    ).order_by('-id')
    
    context = {
        'page_title':f'Search for "{search_term}" | ',
        'search_term':search_term,
        'recipes':recipes,
    }
    return render(
        request,
        'recipes/pages/search.html',
        context=context,
    )