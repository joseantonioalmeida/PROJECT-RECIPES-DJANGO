from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base import RecipeBasePageFunctionalTest
import pytest
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBasePageFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn("No recipes found here", body.text)
    
    
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):

        #cria receitas para testar a busca
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what i need'

        recipes[-1].title = title_needed
        recipes[-1].save()

        # usuário abre a página
        self.browser.get(self.live_server_url)
        
        # ele vê o campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH, "//input[@placeholder='Search for a recipe...']"
        )

        # clica nesse input e digita o termo de busca
        # "Recipe Title 1" para encontrar a receita com esse título
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        search_results = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main-content-list'))
        )

        self.assertIn(title_needed, search_results.text)
        self.sleep(5)