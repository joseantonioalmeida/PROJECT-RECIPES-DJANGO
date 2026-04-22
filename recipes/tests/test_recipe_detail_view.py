from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
   

class RecipeDetailViewTest(RecipeTestBase):     
    #recipe
    def test_recipe_recipe_view_function_is_correct(self):
        view =  resolve(reverse('recipes:recipe', kwargs={'pk':1}))
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipe_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse("recipes:recipe",
                    kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = "This is a detail page - It load one recipe"
        #cria uma receita
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'pk':1}))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipe']

        self.assertIn(needed_title, response_content)


    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        #cria uma receita
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe', 
            kwargs={
                'pk':recipe.id})) #type:ignore
        self.assertEqual(response.status_code, 404)
