from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views, models
from django.contrib.auth.models import User


class RecipeViewsTest(TestCase):
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
    
    def test_recipe_home_loads_recipes(self):
        category = models.Category.objects.create(name='Category Test')
        author = User.objects.create_user(
            first_name='user',
            last_name='user',
            username='user',
            password='user',
            email='user',
        )
        recipe = models.Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )

        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', response_content)
        self.assertIn('10 Minutos', response_content)
        self.assertIn('5 Porções', response_content)
        self.assertEqual(len(response_context_recipes), 1)
        assert 1 == 1

    #category
    def test_recipe_category_view_function_is_corret(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse("recipes:category",
                    kwargs={'category_id': 1000}))
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