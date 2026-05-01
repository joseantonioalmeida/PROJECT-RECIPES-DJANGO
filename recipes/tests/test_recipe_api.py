from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def get_recipe_revese_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_revese_url(reverse_result)
        response = self.client.get(api_url)   
        return response
    
    def get_jwt_access_token(self):
        userdata:dict = {
            'username': 'user',
            'password': 'password'
        }
        author =self.make_author(
            username=userdata.get('username', ''),
            password=userdata.get('password', '')
        )
        response = self.client.post(reverse('recipes:token_obtain_pair'),data={**userdata})
        return response.data.get('access') #type:ignore
    
    def get_recipe_raw_data(self):
        return {
            'title':'This is the title',
            'description':'This is the description',
            'preparation_time':1,
            'preparation_time_unit':'Minutes',
            'servings':1,
            'servings_unit':'Minutes',
            'preparation_steps':'This is the preparation steps',
        }
    
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
            len(response.data.get('results')), #type:ignore
            1
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # Cria as categorias
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')
        # cria 10 receitas
        recipes = self.make_recipe_in_batch(10)
        # muda todas as receitas
        for cont, recipe in enumerate(recipes):
            if cont == 0:
                # muda a category para não desejada
                recipes[0].cagetory = category_not_wanted
            else:
                # muda o restante das recipes com a category desejada
                recipe.category = category_wanted
            recipe.save()

        # ação: pega as receitas pela category_id desejada
        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category_wanted.id}' #type:ignore
        response = self.get_recipe_api_list(reverse_result=api_url)

        # nós devemos ver apenas as receitas que tenha a category desejada
        self.assertEqual(
            len(response.data.get('results')), #type:ignore
            9
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_revese_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )
    
    def test_recipe_api_list_logged_user_can_created_a_recipe(self):
        data = self.get_recipe_raw_data()
        response = self.client.post(
            self.get_recipe_revese_url(), 
            data=data, 
            HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_access_token()}'
        )
        self.assertEqual(
            response.status_code,
            201
        )