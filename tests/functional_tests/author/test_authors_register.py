from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')
    
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)
                
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')
        
        callback(form)
        
        return form
    
    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Digite seu nome...')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            
            form = self.get_form()
            
            self.assertIn('Por favor, Preencha seu nome', form.text)
            
        self.form_field_test_with_callback(callback)
        
    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Digite seu sobrenome...')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            
            form = self.get_form()
            
            self.assertIn('Por favor, Preencha sua sobrenome', form.text)

        self.form_field_test_with_callback(callback)
        
    def test_empty_username_error_message(self):
        def callback(form):
            username = self.get_by_placeholder(form, 'Digite seu nome de usuário...')
            username.send_keys(' ')
            username.send_keys(Keys.ENTER)
            
            form = self.get_form()
            
            self.assertIn('Este campo é obrigatório', form.text)
            
        self.form_field_test_with_callback(callback)
        
    def test_invalid_email_error_message(self):
        def callback(form):
            email = self.get_by_placeholder(form, 'Digite seu e-mail...')
            email.send_keys('email@invalid.com')
            email.send_keys(Keys.ENTER)
            
            form = self.get_form()
            
            self.assertIn('Digite um e-mail válido', form.text)
            
        self.form_field_test_with_callback(callback)
        
    def test_passwords_do_not_message(self):
        def callback(form):
            password = self.get_by_placeholder(form, 'Digite sua senha...')
            confirm_password = self.get_by_placeholder(form, 'Repita sua senha...')
            password.send_keys('Password55')
            confirm_password.send_keys('Password50')
            confirm_password.send_keys(Keys.ENTER)
            
            form = self.get_form()
            

            self.assertIn('Senha e Confirmar senha devem ser iguais', form.text)
            
        self.form_field_test_with_callback(callback)
        
    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        
        self.get_by_placeholder(form, 'Digite seu nome...').send_keys('First')
        self.get_by_placeholder(form, 'Digite seu sobrenome...').send_keys('Last')
        self.get_by_placeholder(form, 'Digite seu nome de usuário...').send_keys('Username')
        self.get_by_placeholder(form, 'Digite seu e-mail...').send_keys('email@valid.com')
        self.get_by_placeholder(form, 'Digite sua senha...').send_keys('Password800')
        self.get_by_placeholder(form, 'Repita sua senha...').send_keys('Password800')
        
        form.submit()

        
        self.assertIn('Usuário cadastrado com sucesso.', self.browser.find_element(By.TAG_NAME, 'body').text)