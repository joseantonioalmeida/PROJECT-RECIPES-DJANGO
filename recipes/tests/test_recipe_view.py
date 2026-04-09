from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
   

class RecipeViewsTest(RecipeTestBase):    
    #home
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.index)

    def test_recipe_home_view_function_status_code_200_ok(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_function_load_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found here',
            response.content.decode('utf-8'),
        )
    
    def test_recipe_home_template_loads_recipes(self):
        #cria uma receita
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', response_content)
        self.assertEqual(len(response_context_recipes), 1)

        assert 1 == 1

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        #cria uma receita
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found here',
            response.content.decode('utf-8'),
        )


    #category
    def test_recipe_category_view_function_is_corret(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertIs(view.func, views.category)

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

        assert 1 == 1
    
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        #cria uma receita
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:category', 
            kwargs={
                'category_id':recipe.category.id})) #type:ignore
        self.assertEqual(response.status_code, 404)

    
    #recipe
    def test_recipe_recipe_view_function_is_correct(self):
        view =  resolve(reverse('recipes:recipe', kwargs={'id':1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse("recipes:recipe",
                    kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = "This is a detail page - It load one recipe"
        #cria uma receita
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1}))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipe']

        self.assertIn(needed_title, response_content)

        assert 1 == 1

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        #cria uma receita
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe', 
            kwargs={
                'id':recipe.id})) #type:ignore
        self.assertEqual(response.status_code, 404)

    # search

    def test_recipe_search_user_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)