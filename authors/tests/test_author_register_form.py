from authors.forms import RegisterForm
from parameterized import parameterized
from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from django.urls import reverse

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