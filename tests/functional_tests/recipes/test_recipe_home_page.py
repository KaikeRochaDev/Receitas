import time
from unittest.mock import patch

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_chrome_browser


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def sleep(self, seconds=5):
        time.sleep(seconds)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita foi encontrada aqui 😞', body.text)
        browser.quit()
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_fund_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        
        title_needed = 'Preciso desse título'
        recipes[0].title = title_needed
        recipes[0].save()
        
        search_input = browser.find_element(By.XPATH, '//input[@placeholder="Procure pelas receitas aqui..."]')
        
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        
        self.assertIn(title_needed, browser.find_element(By.CLASS_NAME, 'main-content-list').text)
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        
        page2 = browser.find_element(By.XPATH, '//a[@aria-label="Ir para a página 2"]')
        
        page2.click()
        
        self.assertEqual(len(browser.find_elements(By.CLASS_NAME, 'recipe')), 2)