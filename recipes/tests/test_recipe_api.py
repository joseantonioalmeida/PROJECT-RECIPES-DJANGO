from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
from unittest.mock import patch



class RecipeAPIv2TestMixin(RecipeMixin):
    def get_recipe_list_revese_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_revese_url(reverse_result)
        response = self.client.get(api_url)   #type:ignore
        return response
    
    def get_auth_data(self, username='user', password='pass'):
        userdata:dict = {
            'username': username,
            'password': password,
        }
        user =self.make_author(
            username=userdata.get('username', ''),
            password=userdata.get('password', '')
        )
        response = self.client.post(reverse('recipes:token_obtain_pair'),data={**userdata}) #type:ignore
        return {
            'jwt_access_token':response.data.get('access'),
            'jwt_refresh_token':response.data.get('refresh'),
            'user':user,
        }
    
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

class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):    
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
        api_url = self.get_recipe_list_revese_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )
    
    def test_recipe_api_list_logged_user_can_created_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        response = self.client.post(
            self.get_recipe_list_revese_url(), 
            data=recipe_raw_data, 
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            201
        )
    
    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        wanted_new_title = f'The new title updated by {author.username}' #type:ignore

        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),  #type:ignore
            data={
                'title': wanted_new_title
            }, 
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.data.get('title'), #type:ignore
            wanted_new_title,
        )
    
    def test_recipe_api_list_logged_user_can_update_a_recipe_owned_by_another_user(self):
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')

        # This user cannot updated the recipe
        another_user = self.get_auth_data(username='cant_update') #type:ignore
        jwt_access_token_from_another_user = another_user.get('jwt_access_token')

        # This is the actual owner of the recipe because it is owned by another user.
        author = access_data.get('user')
        recipe.author = author
        recipe.save()


        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),  #type:ignore
            data={}, 
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token_from_another_user}'
        )

        # another user cannot updated the recipe, so the status code must be 403 Forbidden
        self.assertEqual(
            response.status_code,
            403,
        )