from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Digite seu nome...'),
        ('last_name', 'Digite seu sobrenome...'),
        ('username', 'Digite seu nome de usuário...'),
        ('email', 'Digite seu e-mail...'),
        ('password', 'Digite sua senha...'),
        ('confirm_password', 'Repita sua senha...'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
        
    @parameterized.expand([
        ('username', (
            'O nome de usuário deve conter letras e números. '
            'o Usuário deve conter entre 4 e 150 caracteres.'
        )),
        ('email', 'Digite um e-mail válido')
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
        

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Nome de usuário'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('confirm_password', 'Confirmar senha'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)
        

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'users',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'email@anyemail.com',
            'password': 'Str0ngPassword',
            'confirm_password': 'Str0ngPassword'
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'Este campo é obrigatório'),
        ('first_name', 'Por favor, Preencha seu nome'),
        ('last_name', 'Por favor, Preencha sua sobrenome'),
        ('password', 'Por favor, Preencha sua senha'),
        ('confirm_password', 'Por favor, repita sua senha'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
        
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'O usuário deve conter pelo menos 4 caracteres'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A'*151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'O usuário não pode conter mais do que 150 caracteres'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = (
            'A senha deve ter pelo menos uma letra maiúscula, uma letra minúscula e um número. ' 
            'A senha deve ser de pelo menos 8 caracteres'
        )
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
        self.form_data['password'] = 'Teste123456'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.context['form'].errors.get('password'))
        
    def test_password_and_confirm_password_are_equal(self):
        self.form_data['password'] = 'Teste123456'
        self.form_data['confirm_password'] = 'Teste1234567'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Senha e Confirmar senha devem ser iguais'
        
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
        self.form_data['password'] = 'Teste123456'
        self.form_data['confirm_password'] = 'Teste123456'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.content.decode('utf-8'))
        
    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)