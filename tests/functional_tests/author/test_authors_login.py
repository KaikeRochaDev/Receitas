from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorsLoginTest(AuthorsBaseTest):

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')
    
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(username='my_user', password='pass')
        
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        
        username_field = self.get_by_placeholder(form, 'Digite seu nome de usuário...')
        
        password_field = self.get_by_placeholder(form, 'Digite sua senha...')
        
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)
        
        form.submit()
        
        self.assertIn(f'Você está logado com {user.username}.', self.browser.find_element(By.TAG_NAME, 'body').text)
        