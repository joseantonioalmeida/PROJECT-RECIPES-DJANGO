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
        old_main_content = self.browser.find_element(
            By.CLASS_NAME, 'main-content-list'
        )

        # clica nesse input e digita o termo de busca
        # "Recipe Title 1" para encontrar a receita com esse título
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 15).until(
            EC.staleness_of(old_main_content)
        )

        search_results = WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main-content-list'))
        )

        self.assertIn(title_needed, search_results.text)

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        #cria receitas para testar a busca
        self.make_recipe_in_batch()

        # usuário abre a página
        self.browser.get(self.live_server_url)

        # espera o link da página 2 ficar disponível
        page2 = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Go to page 2"]'))
        )
        # clica via JavaScript para evitar elementos sticky bloquearem o clique
        self.browser.execute_script('arguments[0].click();', page2)

        # espera a página 2 estar ativa antes de verificar os resultados
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Current page 2"]'))
        )

        # vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
        self.sleep(5)