from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
   

class RecipeCategoryViewTest(RecipeTestBase):    
    #category
    def test_recipe_category_view_function_is_corret(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse("recipes:category",
                    kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = "This is a category test"
        #cria uma receita
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn(needed_title, response_content)

    
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        #cria uma receita
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:category', 
            kwargs={
                'category_id':recipe.category.id})) #type:ignore
        self.assertEqual(response.status_code, 404)
