from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def get_recipe_api_list(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)   
        return response
    
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.status_code,
            200
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(wanted_number_of_recipes)
        response = self.get_recipe_api_list()
        qtd_of_load_recipes = len(response.data.get('results')) #type:ignore
        self.assertEqual(
            qtd_of_load_recipes,
            wanted_number_of_recipes
        )

    def test_recipe_api_list_do_not_show_published_recipes(self):
        recipes = self.make_recipe_in_batch(2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        recipe1 = recipes[1]
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.data.get('results'), #type:ignore
            1
        )