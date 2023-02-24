from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    title = forms.CharField(
        error_messages={'required': 'Por favor, Preencha o título'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o título da receita'
        }),
        label='Título'
    )
    
    description = forms.CharField(
        error_messages={'required': 'Por favor, Preencha a descrição.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite a descrição da receita...'
        }),
        label='Descrição'
    )
    
    preparation_time = forms.CharField(
        error_messages={'required': 'Por favor, Preencha o título'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Informe o tempo de preparo...'
        }),
        label='Tempo de preparo'
    )
    
    servings = forms.CharField(
        error_messages={'required': 'Por favor, Preencha o número de porções.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o número de porções...'
        }),
        label='Porções'
    )
    
    preparation_steps = forms.CharField(
        error_messages={'required': 'Por favor, Preencha as etapas de preparação.'},
        widget=forms.Textarea(attrs={
            'placeholder': 'Digite as etapas de preparo...'
        }),
        label='Etapas de preparação'
    )
    
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cd = self.cleaned_data

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self._my_errors['title'].append('Não pode ser igual a descrição.')
            self._my_errors['description'].append('Não pode ser igual ao título.')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('O título deve conter pelo menos 5 caracteres.')

        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Digite um número positivo.')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Digite um número positivo.')

        return field_value