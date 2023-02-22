from django.test import LiveServerTestCase
from utils.browser import make_chrome_browser
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    def sleep(self, seconds=5):
        time.sleep(seconds)
        
    def test_the_test(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        self.sleep(6)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita foi encontrada aqui 😞', body.text)
        browser.quit()