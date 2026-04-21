from django.views import View
from recipes.models import Recipe
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from authors.forms import AuthorRecipeForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch',
)
class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None
        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()
            if not recipe:
                raise Http404()
            
        return recipe
    
    def render_recipe(self, form):
        return render(
            self.request, 
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form,
            }
        )

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)
       
    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )

        if form.is_valid():
            recipe_obj = form.save(commit=False)

            recipe_obj.author = request.user
            recipe_obj.is_published = False
            recipe_obj.preparation_steps_is_html = False
            recipe_obj.save()
            if recipe is not None:
                messages.success(request, 'Recipe updated successfully.')
            else:
                messages.success(request, 'Recipe created successfully.')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe_obj.id,)))
        
        return self.render_recipe(form)       