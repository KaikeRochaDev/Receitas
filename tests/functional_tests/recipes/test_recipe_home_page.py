from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import pytest

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_recipe_home_page_without_recipes_not_found_message(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        
        self.assertIn('Nenhuma receita foi encontrada aqui 😞', body.text)
        browser.quit()