from django import forms 
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'password': 'Senha',
        }
        help_texts = {
            'email': 'Digite um e-mail válido'
        }
        
        error_messages = {
            'username': {
                'required': 'Este campo é obrigatório',
            }
        }
        
        widgets = {
            'first_name': forms.TextInput(),
            
            'last_name': forms.TextInput(),
            
            'username': forms.TextInput(),
            
            'email': forms.EmailInput(),
            
            'password': forms.PasswordInput()
        }
        