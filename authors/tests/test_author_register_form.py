from authors.forms import RegisterForm
from parameterized import parameterized
from unittest import TestCase

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