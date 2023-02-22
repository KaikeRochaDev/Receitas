from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome de usuário...'
        }),
        label='Nome de usuário'
        )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha...'
            }),
        label='Senha'
        )