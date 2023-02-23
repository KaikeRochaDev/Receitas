from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_methor(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        
        response = self.client.get(reverse('authors:logout'), follow=True)
        
        self.assertIn('Solicitação de logout inválida', response.content.decode('utf-8'))
        
    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        
        response = self.client.post(reverse('authors:logout'), data={'username': 'another_user'}, follow=True)
        
        self.assertIn('Usuário de logout inválido', response.content.decode('utf-8'))
        
    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        
        response = self.client.post(reverse('authors:logout'), data={'username': 'my_user'}, follow=True)
        
        self.assertIn('Usuário desconectado com sucesso', response.content.decode('utf-8'))