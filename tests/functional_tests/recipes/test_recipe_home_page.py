from selenium.webdriver.common.by import By
from .base import RecipeBasePageFunctionalTest

class RecipeHomePageFunctionalTest(RecipeBasePageFunctionalTest):

    def test_recipe_home_page_loads(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn("No recipes found here", body.text)
