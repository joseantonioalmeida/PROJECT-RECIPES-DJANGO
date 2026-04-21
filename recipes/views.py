from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.db.models import Q
from utils.pagination import make_pagination
import os
from django.views.generic import ListView

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/pages/home.html'
    ordering = '-id'
    
    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'), 
            PER_PAGE
        )
        ctx.update({'recipes':page_obj,'pagination_range':pagination_range})
        return ctx

def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    page_obj, pagination_range = make_pagination(request,recipes,PER_PAGE)

    context = {
        'recipes': page_obj,
        'pagination_range':pagination_range,
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

    page_obj, pagination_range = make_pagination(request,recipes,PER_PAGE)

    
    context = {
        'page_title':f'Search for "{search_term}" | ',
        'search_term':search_term,
        'recipes':page_obj,
        'pagination_range':pagination_range,
        'additional_url_query':f'&q={search_term}',
    }
    return render(
        request,
        'recipes/pages/search.html',
        context=context,
    )