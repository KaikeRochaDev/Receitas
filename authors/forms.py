from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()
    
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha'
            }),
        label='Confirmar senha',
    )
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
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome...'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu sobrenome...'
            }),
            
            'username': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome de usuário...'
            }),
            
            'email': forms.EmailInput(attrs={
                'placeholder': 'Digite seu e-mail...'
            }),
            
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha...'
            })
        }
        
    def clean_password(self):
        data = self.cleaned_data.get('password')
        
        if 'atenção' in data:
            raise ValidationError(
                'Não digite "atenção" no campo de password',
                code='invalid',
                params={ 'value': 'atenção' }
            )
        
        return data
    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        
        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo nome',
                code='invalid',
                params={ 'value': '"John Doe"' }
            )
        
        return data