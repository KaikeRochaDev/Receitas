from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter pelo menos uma letra maiúscula, uma letra minúscula e um número. ' 
            'A senha deve ser de pelo menos 8 caracteres'
        ),
            code='invalid')

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        error_messages={'required': 'Por favor, Preencha seu nome'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome...'
        }),
        label='Nome'
    )
    
    last_name = forms.CharField(
        error_messages={'required': 'Por favor, Preencha sua sobrenome'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu sobrenome...'
        }),
        label='Sobrenome'
    )
    
    username = forms.CharField(
        error_messages={'required': 'Este campo é obrigatório', 'min_length': 'O usuário deve conter pelo menos 4 caracteres', 'max_length': 'O usuário não pode conter mais do que 150 caracteres'},
        help_text=(
            'O nome de usuário deve conter letras e números. '
            'o Usuário deve conter entre 4 e 150 caracteres.'
        ),
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu nome de usuário...'
        }),
        label='Nome de usuário',
        min_length=4, max_length=150
    )
    
    email = forms.CharField(
        error_messages={'required': 'Por favor, Preencha seu e-mail'},
        help_text='Digite um e-mail válido',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu e-mail...'
        }),
        label='E-mail'
    )
    
    password = forms.CharField(
        error_messages={'required': 'Por favor, Preencha sua senha'},
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha...'
            }),
        label='Senha',
        validators=[strong_password]
    )
    
    
    confirm_password = forms.CharField(
        error_messages={'required': 'Por favor, repita sua senha'},
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha...'
            }),
        label='Confirmar senha',
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise ValidationError({
                'password': 'Senha e Confirmar senha devem ser iguais',
                
                'confirm_password': 'Senha e Confirmar senha devem ser iguais'
            })