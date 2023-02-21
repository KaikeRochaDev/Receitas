from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Digite seu nome...'),
        ('last_name', 'Digite seu sobrenome...'),
        ('username', 'Digite seu nome de usuário...'),
        ('email', 'Digite seu e-mail...'),
        ('password', 'Digite sua senha...'),
        ('confirm_password', 'Repita sua senha...'),
    ])
    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)